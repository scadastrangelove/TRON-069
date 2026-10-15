"""Validate independent research aggregates against their fixed Shodan reference."""
import json
import re
from datetime import date


def read_comparison(root, registry):
    read = lambda path: json.loads(path.read_text(encoding='utf-8'))
    data = read(root/'data/index-comparison.json')
    if (set(data) != {'schema_version', 'research_date', 'reviewed', 'provenance',
                     'reference_snapshot', 'source', 'signatures', 'countries'}
            or data['schema_version'] != 1 or data['provenance'] != 'dated-research-summary'):
        raise ValueError('Invalid comparison schema or provenance')
    for field in ('research_date', 'reviewed'):
        date.fromisoformat(data[field])
    if not re.fullmatch(r'\d{8}-\d{4,6}', data['reference_snapshot']):
        raise ValueError('Invalid comparison snapshot')
    snapshot = root/'data/mapdata'/('snapshot-'+data['reference_snapshot'])
    manifest = read(snapshot/'manifest.json')
    if manifest.get('status') != 'complete' or manifest.get('errors'):
        raise ValueError('Comparison requires a complete reference snapshot')
    if data['source'] != {'file': 'CROSS-INDEX.md', 'anchor': 'method'}:
        raise ValueError('Invalid comparison source')

    def counts(row):
        if any(type(row[k]) is not int or row[k] < 0 for k in ('fofa_count', 'shodan_count')):
            raise ValueError('Comparison counts must be non-negative integers')

    ids = set()
    for row in data['signatures']:
        if set(row) != {'line', 'fofa_query_notation', 'fofa_count', 'shodan_query', 'shodan_count', 'shodan_taken'}:
            raise ValueError('Unexpected comparison signature fields')
        slug = row['line']
        if slug not in registry or slug in ids or not re.fullmatch('[a-z0-9-]+', slug):
            raise ValueError('Invalid or duplicate comparison line')
        ids.add(slug)
        counts(row)
        if not isinstance(row['fofa_query_notation'], str) or not row['fofa_query_notation'].strip():
            raise ValueError('Missing FOFA research query notation')
        ref = read(snapshot/(slug+'.json'))
        if (ref.get('collection_status') != 'ok'
                or (row['shodan_query'], row['shodan_count'], row['shodan_taken'])
                != (ref['dork'], ref['total'], ref['taken'])):
            raise ValueError('Comparison signature differs from its reference snapshot')
    park = read(snapshot/'denominator-park.json')
    if park.get('collection_status') != 'ok' or park['dork'] != 'port:7547':
        raise ValueError('Invalid comparison port reference')
    countries = {row['value']: row['count'] for row in park['countries']}
    seen = set()
    for row in data['countries']:
        if set(row) != {'country', 'port', 'fofa_count', 'shodan_count', 'shodan_taken'}:
            raise ValueError('Unexpected comparison country fields')
        cc = row['country']
        if not re.fullmatch('[A-Z]{2}', cc) or cc not in countries or cc in seen or row['port'] != 7547:
            raise ValueError('Invalid or duplicate comparison country scope')
        seen.add(cc)
        counts(row)
        if (row['shodan_count'], row['shodan_taken']) != (countries[cc], park['taken']):
            raise ValueError('Comparison country differs from its reference snapshot')
    return data
