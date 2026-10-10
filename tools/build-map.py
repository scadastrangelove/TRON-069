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
    'huaweihomegateway', 'gsoap-2-7-vendor-map', 'gsoap-2-8-vendor-map',
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

def build(snapshot, output_root=ROOT):
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
    facts = manifest.get('plan', {}).get('facts')
    if facts is None:
        # Older snapshots predate frozen observations. Only use exact matching
        # records; an old handwritten count is never presented as a fresh result.
        facts = bind_facts(read(ROOT/'data/mapdata/facts.json'),
            [dict(id=slug,query=row['shodan_dork']) for slug,row in registry.items()],
            read(ROOT/'data/collection-queries.json')['queries'], strict=False)
    unknown_facts = set(facts) - set(registry)
    if unknown_facts:
        raise ValueError(f'Unknown fact line IDs: {sorted(unknown_facts)}')
    facts = collected_facts(facts, snapshot, read_optional)
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
    }
    validate_translations(data)
    validate_sources(data)
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
    print(f'Built both entry points: {len(lines)} lines, {len(orgdrill)} operator pairs, {len(html.encode()):,} bytes each')
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
