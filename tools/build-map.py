#!/usr/bin/env python3
"""Build both standalone atlas entry points from versioned inputs, without network access."""
import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path
import sys
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collection_catalog import bind_facts, collected_facts
from snapshot_history import snapshot_history, write_history

ROOT = Path(__file__).resolve().parent.parent
IDENT_EXCLUDE = {
    'huaweihomegateway-cr-slice', 'gsoap-2-7-vendor-map', 'gsoap-2-8-vendor-map',
    'sky-ee-tr069-http-server', 'windtre-tr069-http-server', 'sagemcom',
    'genieacs-admin-ui', 'openacs', 'axiros', 'magticom-gsoap',
    'decimal-nonce-class', 'mini-web-server-1-0-zte-corp',
}

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def validate_translations(data):
    """Fail the build instead of silently shipping Russian editorial fallback."""
    strings = []
    for meta in data['meta']['lines'].values():
        for key in ('vendor', 'role', 'findings', 'anomalies', 'overlaps'):
            value = meta.get(key, [])
            strings.extend(value if isinstance(value, list) else [value])
    def collect(value):
        if isinstance(value, str):
            strings.append(value)
        elif isinstance(value, dict):
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)
    collect(data['facts'])
    strings.extend(rule['norm'] for rule in data['orgnorm']['rules'])
    missing = [s for s in strings if isinstance(s, str) and re.search('[А-Яа-яЁё]', s)
               and any(not data['translations'].get(s, {}).get(lang) for lang in ('en', 'es', 'zh'))]
    if missing:
        raise ValueError(f'Missing content translations: {missing}')

def read_news():
    news = read(ROOT/'data/project-news.json')
    ids = set()
    for item in news:
        if not re.fullmatch('[a-z0-9-]+', item['id']) or item['id'] in ids:
            raise ValueError('Invalid or duplicate news ID')
        ids.add(item['id'])
        date.fromisoformat(item['date'])
        if item['kind'] not in ('atlas', 'research', 'data'):
            raise ValueError('Unknown news category')
        if item.get('view') not in (None, 'ecosystem'):
            raise ValueError('Unknown news view')
        if not isinstance(item.get('pinned', False), bool):
            raise ValueError('News pinned flag must be boolean')
        for link in item.get('links', []):
            url = link.get('url', '')
            parsed = urlsplit(url)
            if (parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password
                    or any(c.isspace() or ord(c) < 32 for c in url) or not link.get('label', '').strip()):
                raise ValueError('Invalid news link')
        for field in ('title', 'body'):
            if any(not isinstance(item[field].get(lang), str) or not item[field][lang].strip()
                   for lang in ('ru', 'en', 'es', 'zh')):
                raise ValueError(f'Missing news translation: {item["id"]}/{field}')
        if not item.get('evidence'):
            raise ValueError(f'Missing news evidence: {item["id"]}')
        for evidence in item['evidence']:
            path = (ROOT/evidence['file']).resolve()
            if not path.is_relative_to(ROOT) or not path.is_file():
                raise ValueError(f'Invalid news evidence file: {item["id"]}')
    if sum(item.get('pinned', False) for item in news) > 1:
        raise ValueError('Only one news item may be pinned')
    return sorted(news, key=lambda item: (item.get('pinned', False), item['date']), reverse=True)


def validate_sources(data):
    references = [s for m in data['meta']['lines'].values() for s in m.get('sources', [])]
    references += [s for items in data['facts'].values() for f in items for s in f.get('sources', [])]
    references += [v['source'] for items in data['variants'].values() for v in items if v.get('source')]
    references += [s for n in data['news'] for s in n['evidence']]
    references += [s for e in data.get('ecosystem', {}).get('edges', [])
                   for s in e['sources'] if 'file' in s]
    for source in references:
        name = source.get('file', '')
        path = (ROOT/name).resolve()
        if (not re.fullmatch(r'[a-zA-Z0-9_./-]+', name) or any(p in ('', '..') for p in name.split('/'))
                or not path.is_relative_to(ROOT) or not path.is_file()):
            raise ValueError(f'Invalid public source reference: {name}')
        anchor = source.get('anchor')
        if anchor and (not re.fullmatch(r'[a-zA-Z0-9_.-]+', anchor)
                       or f'id="{anchor}"' not in path.read_text(encoding='utf-8')):
            raise ValueError(f'Missing public source anchor: {name}#{anchor}')


def read_ecosystem(registry):
    catalog = read(ROOT/'data/acs-relations.json')
    operator_ids = {op['id'] for op in read_operators()['operators']}
    if catalog.get('schema_version') != 1:
        raise ValueError('Unknown ecosystem schema')
    date.fromisoformat(catalog['reviewed'])
    def localized(value):
        return (isinstance(value, dict) and all(isinstance(value.get(lang), str)
                and value[lang].strip() for lang in ('en', 'ru', 'es', 'zh')))
    def identifiers(items):
        ids = [item['id'] for item in items]
        if len(set(ids)) != len(ids) or any(not re.fullmatch('[a-z0-9-]+', i) for i in ids):
            raise ValueError('Invalid or duplicate ecosystem ID')
        return set(ids)
    nodes = identifiers(catalog['nodes'])
    identifiers(catalog['edges'])
    for node in catalog['nodes']:
        if set(node) - {'id', 'kind', 'name', 'description', 'line', 'operator'}:
            raise ValueError('Unknown ecosystem node fields')
        if node.get('operator') and (node['kind'] != 'operator' or node['operator'] not in operator_ids):
            raise ValueError('Invalid ecosystem operator reference')
        if node['kind'] not in ('cpe', 'operator', 'acs', 'endpoint'):
            raise ValueError('Unknown ecosystem node kind')
        if not localized(node['description']) or not (localized(node['name']) or
                isinstance(node['name'], str) and node['name'].strip()):
            raise ValueError('Missing ecosystem translation')
        if 'line' in node and (node['line'] not in registry or
                registry[node['line']]['service'] != node['kind']):
            raise ValueError('Invalid ecosystem registry role')
    for edge in catalog['edges']:
        if set(edge) - {'id', 'source', 'target', 'kind', 'status', 'reviewed', 'observed', 'summary', 'sources', 'map', 'scope'}:
            raise ValueError('Unknown ecosystem edge fields')
        if edge['source'] not in nodes or edge['target'] not in nodes or edge['source'] == edge['target']:
            raise ValueError('Dangling or self-referencing ecosystem edge')
        if edge['kind'] not in ('interop', 'architecture', 'deployment', 'configuration', 'operator', 'attribution'):
            raise ValueError('Unknown ecosystem relationship kind')
        if edge['status'] not in ('documented', 'observed', 'reported', 'hypothesis'):
            raise ValueError('Unknown ecosystem evidence status')
        if not localized(edge['summary']):
            raise ValueError('Missing ecosystem translation')
        for field in ('observed', 'reviewed'):
            date.fromisoformat(edge[field])
        if edge['observed'] > edge['reviewed']:
            raise ValueError('Ecosystem evidence postdates review')
        if not edge['sources']:
            raise ValueError('Missing ecosystem sources')
        for source in edge['sources']:
            if ('file' in source) == ('url' in source) or set(source) - {'file', 'anchor', 'url', 'title'}:
                raise ValueError('Invalid ecosystem source')
            if 'file' in source:
                path = Path(source['file'])
                if (path.suffix not in ('.md', '.json') or any(part.startswith('.') or
                        part in ('private', 'research-private', 'firmware-extracts', 'probes') for part in path.parts)):
                    raise ValueError('Non-public ecosystem source')
            else:
                raw = source['url']
                url = urlsplit(raw)
                if (url.scheme != 'https' or not url.hostname or url.username or url.password or
                        any(c.isspace() or ord(c) < 32 for c in raw) or not source.get('title', '').strip()):
                    raise ValueError('Invalid ecosystem URL')
        scope = edge.get('map')
        if scope:
            linked = {n.get('line') for n in catalog['nodes'] if n['id'] in (edge['source'], edge['target'])}
            if (set(scope) != {'line', 'country'} or scope['line'] not in linked or
                    scope['line'] not in registry or not re.fullmatch('[A-Z]{2}', scope['country'])):
                raise ValueError('Invalid ecosystem map scope')
        scope = edge.get('scope')
        if scope and (set(scope) != {'line', 'country', 'operator'} or scope['line'] not in registry
                      or not re.fullmatch('[A-Z]{2}', scope['country']) or scope['operator'] not in operator_ids):
            raise ValueError('Invalid ecosystem deployment scope')
    return catalog


def read_operators():
    catalog = read(ROOT/'data/operator-catalog.json')
    if catalog.get('schema_version') != 1:
        raise ValueError('Unknown operator catalog schema')
    date.fromisoformat(catalog['reviewed'])
    ids, aliases = set(), set()
    groups = {group['id'] for group in catalog['groups']}
    if len(groups) != len(catalog['groups']):
        raise ValueError('Duplicate operator group')
    for group in catalog['groups']:
        if not re.fullmatch('[a-z0-9-]+', group['id']) or not group['name'].strip():
            raise ValueError('Invalid operator group')
        source = group['source']
        url = urlsplit(source['url'])
        if (url.scheme != 'https' or not url.hostname or url.username or url.password or
                any(c.isspace() or ord(c) < 32 for c in source['url']) or not source['title'].strip()):
            raise ValueError('Invalid operator group source')
    for operator in catalog['operators']:
        if (not re.fullmatch('[a-z0-9-]+', operator['id']) or operator['id'] in ids or
                not operator['name'].strip() or not re.fullmatch('[A-Z]{2}', operator['country'])):
            raise ValueError('Invalid or duplicate operator ID')
        ids.add(operator['id'])
        if operator.get('group') and operator['group'] not in groups:
            raise ValueError('Unknown operator group')
        if not operator['aliases']:
            raise ValueError('Missing operator aliases')
        for alias in operator['aliases']:
            key = (operator['country'], alias.strip().lower())
            if not alias.strip() or key in aliases:
                raise ValueError('Ambiguous operator alias')
            aliases.add(key)
    return catalog

def read_variants(snapshot, manifest, lines):
    records = {}
    for path in sorted((snapshot/'variants').glob('*.json')):
        item = read(path)
        if item.get('collection_status') != 'ok':
            raise ValueError(f'Incomplete variant: {path.name}')
        if item.get('parent') in lines:
            records[item['id']] = item
    for job in manifest.get('plan', {}).get('queries', []):
        item = records.get(job['id'])
        if not item or item['dork'] != job['query'] or item['requested_facets'] != job['facets'] or item.get('run_id') != manifest['plan']['id']:
            raise ValueError(f'Missing or outdated planned variant: {job["id"]}')
    out = {}
    ordered = list(dict.fromkeys([q['id'] for q in manifest.get('plan', {}).get('queries', [])] + list(records)))
    for ident in ordered:
        item = records[ident]
        baseline = records.get(item.get('denominator'))
        item['share'] = (item['total']/baseline['total'] if baseline and baseline['total']
                         and baseline.get('run_id') == item.get('run_id') else None)
        item['denominator_total'] = baseline['total'] if baseline else None
        out.setdefault(item['parent'], []).append(item)
    return out

def refresh_fact_commentary(facts, current_facts):
    """Apply current research notes to the same observation, preserving its measurements.

    Frozen plans remain the source of queries and collection references. Both
    the label and exact query must match before reusing editorial commentary.
    """
    for parent, items in facts.items():
        current = {(item.get('label'), item.get('dork')): item
                   for item in current_facts.get(parent, [])}
        for item in items:
            editorial = current.get((item.get('label'), item.get('dork')), {})
            for key in ('note', 'sources'):
                if key in editorial:
                    item[key] = editorial[key]


def build_data(snapshot):
    manifest = read(snapshot / 'manifest.json')
    if manifest.get('status', 'complete') != 'complete':
        raise ValueError('Refusing to publish an incomplete snapshot checkpoint')
    if manifest.get('errors') or any(r.get('collection_status') != 'ok' for r in manifest['lines']):
        raise ValueError('Refusing to publish an incomplete snapshot')
    meta = read(ROOT / 'data/mapmeta.json')
    with (ROOT/'registry.csv').open(newline='', encoding='utf-8') as stream:
        registry = {r['id']:r for r in csv.DictReader(stream)}
        services = {slug:r['service'] for slug,r in registry.items()}
    if any(s not in ('cpe','acs','mixed','unknown') for s in services.values()):
        raise ValueError('Invalid service classification')
    current_facts = read(ROOT/'data/mapdata/facts.json')
    facts = manifest.get('plan', {}).get('facts')
    if facts is None:
        # Older snapshots predate frozen observations. Only use exact matching
        # records; an old handwritten count is never presented as a fresh result.
        facts = bind_facts(current_facts,
            [dict(id=slug,query=row['shodan_dork']) for slug,row in registry.items()],
            read(ROOT/'data/collection-queries.json')['queries'], strict=False)
    unknown_facts = set(facts) - set(registry)
    if unknown_facts:
        raise ValueError(f'Unknown fact line IDs: {sorted(unknown_facts)}')
    facts = collected_facts(facts, snapshot, read_optional)
    refresh_fact_commentary(facts, current_facts)
    excluded = IDENT_EXCLUDE | {s for s,kind in services.items() if kind == 'acs'}
    lines, ident = {}, {}
    excluded_files = {'manifest.json', 'denominator-park.json', 'denominator-http.json', 'stickers.json'}
    actual_files = {f.name for f in snapshot.glob('*.json')} - excluded_files
    expected_files = {row['file'] for row in manifest['lines']} - excluded_files
    if actual_files != expected_files:
        raise ValueError(f'Snapshot files differ from manifest: {actual_files ^ expected_files}')
    for f in sorted(snapshot.glob('*.json')):
        if f.name in excluded_files:
            continue
        rec = read(f)
        if rec.get('collection_status') != 'ok':
            raise ValueError(f'Incomplete record: {f.name}')
        countries = {c['value']: c['count'] for c in rec['countries']}
        lines[f.stem] = {k: rec[k] for k in ('name', 'dork', 'total')}
        lines[f.stem]['name'] = registry.get(f.stem, {}).get('product', rec['name'])
        lines[f.stem].update(countries=countries, ports=rec.get('ports', []),
            service=services.get(f.stem, 'unknown'),
            nonce=meta['lines'].get(f.stem, {}).get('nonce'),
            taken=rec.get('taken'), collection_status=rec['collection_status'],
            facet_meta=rec.get('facet_meta', {}),
            unknown_country=max(0, rec['total'] - sum(countries.values())))
        if f.stem not in excluded:
            for cc, n in countries.items():
                ident[cc] = ident.get(cc, 0) + n
    denominators = {k: read(snapshot / f'denominator-{k}.json') for k in ('park', 'http')}
    if any(rec.get('collection_status') != 'ok' for rec in denominators.values()):
        raise ValueError('Incomplete denominator')
    names = {v['name']: k for k, v in lines.items()}
    orgdrill = {}
    for f in sorted((snapshot / 'org-drill').glob('*.json')):
        cell = read(f)
        slug = cell.get('line_id') or f.stem.rsplit('--',1)[0]
        if slug not in lines:
            slug = names.get(cell.get('line'))
        if slug in lines and cell.get('collection_status') == 'ok':
            orgdrill[f"{slug}--{cell['cc']}"] = cell
    data = {
        'snapshot': snapshot.name.removeprefix('snapshot-'),
        **{k: {c['value']: c['count'] for c in v['countries']} for k,v in denominators.items()},
        'denominators': denominators, 'ident': ident, 'lines': lines,
        'excluded': sorted(excluded), 'orgdrill': orgdrill,
        'variants': read_variants(snapshot, manifest, lines),
        'collection': manifest.get('org_drill'),
        'stickers': read(snapshot/'stickers.json') if (snapshot/'stickers.json').exists() else {},
        'meta': meta, 'orgnorm': read(ROOT/'data/orgnorm.json'),
        'geo': read(ROOT/'data/world.geojson'), 'facts': facts,
        'translations': read(ROOT/'data/content-i18n.json'),
        'news': read_news(),
        'ecosystem': read_ecosystem(registry),
        'operatorCatalog': read_operators(),
    }
    validate_translations(data)
    validate_sources(data)
    return data


SNAPSHOT_FIELDS = ('snapshot', 'park', 'http', 'denominators', 'ident', 'lines',
                   'excluded', 'orgdrill', 'variants', 'collection', 'stickers', 'facts')


def build(snapshot, output_root=ROOT):
    data = build_data(snapshot)
    # Keep the current atlas self-contained. Historical measurements are loaded
    # on demand; geography and editorial material are shared by every date.
    archives = {}
    for entry in snapshot_history(ROOT/'data/mapdata')['snapshots']:
        if entry['status'] != 'complete' or entry['errors']:
            continue
        path = ROOT/'data/mapdata'/entry['snapshot']
        manifest = read(path/'manifest.json')
        # The earliest legacy dump has no validated collection statuses.
        if any(row.get('collection_status') != 'ok' for row in manifest['lines']):
            continue
        item = data if path.resolve() == snapshot.resolve() else build_data(path)
        archives[item['snapshot']] = item
    archives[data['snapshot']] = data
    entries, line_catalog, countries, orgs = [], {}, set(), {}
    for ident, item in sorted(archives.items(), reverse=True):
        entries.append(dict(id=ident, lines=len(item['lines'])))
        for slug, line in item['lines'].items():
            line_catalog.setdefault(slug, {key: line[key] for key in ('name', 'dork', 'service')})
            countries.update(line['countries'])
        countries.update(item['park'])
        for cell in item['orgdrill'].values():
            orgs.setdefault(cell['cc'], set()).update(org['value'] for org in cell['orgs'])
    data['history'] = dict(snapshots=entries, latest=entries[0]['id'], lines=line_catalog,
                           countries=sorted(countries), orgs={cc: sorted(names) for cc, names in sorted(orgs.items())})
    for ident, item in archives.items():
        out = output_root/'atlas/snapshots'/f'{ident}.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({key: item[key] for key in SNAPSHOT_FIELDS},
                                 ensure_ascii=False, separators=(',', ':'))+'\n', encoding='utf-8')
    template = (ROOT/'atlas/map-template.html').read_text(encoding='utf-8')
    if template.count('/*__DATA__*/{}') != 1:
        raise ValueError('Template must contain exactly one DATA placeholder')
    if template.count('/*__UI__*/{}') != 1:
        raise ValueError('Template must contain exactly one UI placeholder')
    ui = json.dumps(read(ROOT/'data/ui-i18n.json'), ensure_ascii=False).replace('<', '\\u003c')
    template = template.replace('/*__UI__*/{}', ui)
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    html = template.replace('/*__DATA__*/{}', payload)
    for relative in ('index.html', 'atlas/tr-atlas.html'):
        out = output_root/relative
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding='utf-8')
    print(f'Built both entry points: {len(data["lines"])} lines, {len(data["orgdrill"])} operator pairs, '
          f'{len(html.encode()):,} bytes each; {len(archives)} selectable snapshots')
    return data


def read_optional(path):
    return read(path) if path.is_file() else None

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('snapshot', nargs='?', type=Path)
    ap.add_argument('--output-dir', type=Path, default=ROOT)
    args = ap.parse_args()
    history = snapshot_history(ROOT/'data/mapdata')
    snapshot = args.snapshot or (ROOT/'data/mapdata'/history['latest_complete'] if history['latest_complete'] else None)
    if snapshot is None:
        ap.error('No snapshots in data/mapdata')
    build(snapshot.resolve(), args.output_dir.resolve())
    if args.output_dir.resolve() == ROOT:
        write_history(ROOT/'data/mapdata')

if __name__ == '__main__':
    main()
