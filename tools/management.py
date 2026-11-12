"""Public management-plane evidence and dated, passive discovery measurements.

This module only reads the reviewed public catalogs. It never imports a firmware
manifest, credentials, extracted images, host records or private research files.
"""
import json
import re
from datetime import date, datetime

LANGS = ('en', 'ru', 'es', 'zh')
FACETS = {'country', 'org', 'asn', 'port', 'ssl.cert.fingerprint'}


def localized(value):
    return isinstance(value, dict) and all(isinstance(value.get(k), str) and value[k].strip() for k in LANGS)


def source(root, value):
    if set(value) - {'file', 'anchor', 'title'} or 'file' not in value:
        raise ValueError('Invalid management evidence source')
    path = (root/value['file']).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file() or path.suffix not in ('.md', '.json'):
        raise ValueError('Invalid management evidence path')
    if any(p.startswith('.') or p in ('private', 'research-private', 'firmware-extracts', 'probes') for p in path.relative_to(root.resolve()).parts):
        raise ValueError('Non-public management evidence')
    if value.get('anchor') and f'id="{value["anchor"]}"' not in path.read_text():
        raise ValueError('Missing management evidence anchor')


def infrastructure_jobs(root):
    catalog = json.loads((root/'data/infrastructure-queries.json').read_text())
    if catalog.get('schema_version') != 1:
        raise ValueError('Unknown infrastructure catalog schema')
    seen = set()
    for item in catalog['queries']:
        if set(item) != {'id', 'group', 'query', 'facets', 'label', 'source', 'classification'}:
            raise ValueError('Unknown infrastructure query fields')
        if not re.fullmatch('[a-z0-9-]+', item['id']) or item['id'] in seen:
            raise ValueError('Invalid infrastructure query ID')
        seen.add(item['id'])
        if item['group'] != 'management-infrastructure' or not item['query'].startswith('ssl.cert.'):
            raise ValueError('Invalid infrastructure query scope')
        if item['classification'] not in ('acs-candidate', 'issuer-match', 'broad-discovery') or not localized(item['label']):
            raise ValueError('Invalid infrastructure query classification')
        fields = item['facets'].split(',')
        for field in fields:
            name, limit = field.rsplit(':', 1)
            if name not in FACETS or not limit.isdigit() or not 1 <= int(limit) <= 1000:
                raise ValueError('Invalid infrastructure facet')
        if len({f.rsplit(':', 1)[0] for f in fields}) != len(fields):
            raise ValueError('Duplicate infrastructure facet')
        source(root, item['source'])
    return catalog['queries']


def read_evidence(root, registry):
    data = json.loads((root/'data/management-evidence.json').read_text())
    if set(data) != {'schema_version', 'reviewed', 'platform', 'profiles'} or data['schema_version'] != 1:
        raise ValueError('Unknown management evidence schema')
    date.fromisoformat(data['reviewed'])
    platform = data['platform']
    if set(platform) != {'id', 'name', 'line', 'profile_count', 'data_model_count', 'source', 'gaps'} or platform['line'] not in registry:
        raise ValueError('Invalid management platform')
    if any(type(platform[k]) is not int or platform[k] < 1 for k in ('profile_count', 'data_model_count')):
        raise ValueError('Invalid firmware inventory counts')
    source(root, platform['source'])
    if set(platform['gaps']) - {'artifact-source', 'artifact-version', 'artifact-hash', 'profile-deduplication'}:
        raise ValueError('Invalid management platform gap')
    queries = {q['id']: q for q in json.loads((root/'data/collection-queries.json').read_text())['queries']}
    seen = set()
    for profile in data['profiles']:
        if set(profile) != {'id', 'profile', 'country', 'operator_hint', 'operator_status', 'port', 'query_id', 'source'}:
            raise ValueError('Unknown management profile fields')
        if not re.fullmatch('[a-z0-9-]+', profile['id']) or profile['id'] in seen:
            raise ValueError('Invalid management profile ID')
        seen.add(profile['id'])
        if not re.fullmatch('[A-Z]{2}', profile['country']) or not 1 <= profile['port'] <= 65535:
            raise ValueError('Invalid management profile scope')
        if profile['operator_status'] != 'unverified' or not profile['operator_hint'].strip():
            raise ValueError('Operator identity needs reviewed evidence before promotion')
        query = queries.get(profile['query_id'], {})
        expected = f'{registry[platform["line"]]["shodan_dork"]} port:{profile["port"]} country:{profile["country"]}'
        if query.get('parent') != platform['line'] or query.get('query') != expected:
            raise ValueError('Management profile query must bind line, port and country')
        source(root, profile['source'])
    return data


def read_measurements(snapshot, manifest):
    """A result belongs to this snapshot; never fall forward to a newer date."""
    records = {}
    for path in sorted((snapshot/'infrastructure').glob('*.json')):
        record = json.loads(path.read_text())
        allowed = {'id', 'group', 'label', 'source', 'classification', 'dork', 'total', 'taken', 'run_id',
                   'collection_status', 'requested_facets', 'facet_meta', 'countries', 'orgs', 'asn', 'ports', 'fingerprints'}
        if set(record) - allowed or record.get('id') != path.stem or record.get('collection_status') != 'ok':
            raise ValueError('Invalid infrastructure measurement')
        if type(record.get('total')) is not int or record['total'] < 0:
            raise ValueError('Invalid infrastructure total')
        if datetime.fromisoformat(record['taken'].replace('Z', '+00:00')).tzinfo is None:
            raise ValueError('Infrastructure timestamp needs timezone')
        if not localized(record.get('label')) or record.get('classification') not in ('acs-candidate', 'issuer-match', 'broad-discovery'):
            raise ValueError('Invalid infrastructure measurement metadata')
        for key in ('countries', 'orgs', 'asn', 'ports', 'fingerprints'):
            if any(set(v) != {'value', 'count'} or type(v['count']) is not int or v['count'] < 0 for v in record.get(key, [])):
                raise ValueError('Invalid infrastructure aggregate')
        records[record['id']] = record
    for job in manifest.get('plan', {}).get('infrastructure_queries', []):
        record = records.get(job['id'])
        if not record or record['dork'] != job['query'] or record['requested_facets'] != job['facets'] or record['run_id'] != manifest['plan']['id']:
            raise ValueError(f'Missing or outdated infrastructure result: {job["id"]}')
    return records


def profile_measurements(evidence, variants):
    records = {r['id']: r for rows in variants.values() for r in rows}
    result = {}
    for profile in evidence['profiles']:
        record = records.get(profile['query_id'])
        # The country/port intersection is a measurement, not operator attribution.
        result[profile['id']] = dict(query_id=profile['query_id'],
            status='observed' if record and record['total'] else 'not-observed' if record else 'not-collected',
            total=record['total'] if record else None, taken=record.get('taken') if record else None,
            orgs=record.get('orgs', []) if record else [],
            remainder=record.get('facet_meta', {}).get('org', {}).get('remainder') if record else None)
    return result
