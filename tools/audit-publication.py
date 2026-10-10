#!/usr/bin/env python3
"""Read-only public-tree checks; run in addition to human disclosure review."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent


def main():
    errors = []
    files = [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts]
    for p in files:
        relative = p.relative_to(ROOT)
        if p.is_symlink():
            errors.append(f'Symlink needs review: {relative}')
        if set(relative.parts) & {'firmware-extracts', 'probes', '.publication', 'private', 'research-private'}:
            errors.append(f'Private directory: {relative}')
        if p.suffix in {'.bin', '.rbi', '.img', '.gz', '.jsonl', '.pem', '.key', '.log'} or p.name.startswith('.env'):
            errors.append(f'Non-public artifact: {relative}')
    docs = [p for p in files if p.suffix.lower() == '.md']
    for p in docs:
        text = p.read_text(encoding='utf-8')
        if re.search('[А-Яа-яЁё]', text):
            errors.append(f'Untranslated Markdown: {p.relative_to(ROOT)}')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            url = urlsplit(target)
            if url.scheme or target.startswith('#'):
                continue
            dest = (p.parent / unquote(url.path)).resolve()
            if not dest.is_relative_to(ROOT) or not dest.exists():
                errors.append(f'Broken local link in {p.relative_to(ROOT)}: {target}')
    read = lambda name: json.loads((ROOT/name).read_text(encoding='utf-8'))
    coverage = read('data/research-findings.json')
    meta = read('data/mapmeta.json')['lines']
    catalog = read('data/collection-queries.json')['queries']
    news = {n['id']: n for n in read('data/project-news.json')}
    if set(coverage['line_sources']) != set(meta):
        errors.append('Line/source coverage differs from the registry metadata')
    if set(coverage['catalog_query_ids']) != {q['id'] for q in catalog}:
        errors.append('Research catalog coverage differs from the catalog')
    for item in coverage['findings']:
        if any(line not in meta for line in item['lines']):
            errors.append(f'Unknown finding line: {item["id"]}')
        if item['news_id'] not in news or not (ROOT/item['source']).is_file():
            errors.append(f'Missing finding news/source: {item["id"]}')
    for name in ('LICENSE', 'NOTICE'):
        if not (ROOT/name).is_file():
            errors.append(f'Missing {name}')
    if (ROOT/'index.html').read_bytes() != (ROOT/'atlas/tr-atlas.html').read_bytes():
        errors.append('Atlas entry points differ')
    print(json.dumps({'markdown_files': len(docs), 'research_findings': len(coverage['findings']),
                      'lines': len(meta), 'queries': len(catalog), 'errors': errors}, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
