"""Editorial inventory of inspected artifacts, bounded negatives and research leads."""
import copy
import json
import re
from datetime import date

STATUSES = {'matched': 'Match in sample', 'negative': 'Scoped negative',
            'partial': 'Partial extraction', 'pending': 'Awaiting verification'}
KINDS = {'image': 'Firmware image', 'source': 'Source code',
         'binary': 'Binary / dump', 'container': 'Firmware container'}
VERIFICATIONS = {'reproduced': 'Artifact checked', 'documented': 'Published research note',
                 'reported': 'Reported lead'}
MISSING = {'source': 'public artifact source', 'version': 'exact release / revision',
           'hash': 'binary hash', 'template': 'CR-template comparison', 'variant': 'hardware variant'}


def read_specimens(root, registry, attributions):
    catalog = json.loads((root/'data/research-specimens.json').read_text(encoding='utf-8'))
    if catalog.get('schema_version') != 1 or not isinstance(catalog.get('items'), list):
        raise ValueError('Invalid specimen catalog')
    date.fromisoformat(catalog['reviewed_at'])
    anchors = {item['id']: item for item in attributions['items']}
    seen = set()
    for item in catalog['items']:
        ident = item.get('id', '')
        if (not re.fullmatch('[a-z0-9-]+', ident) or ident in seen
                or not isinstance(item.get('title'), str) or not item['title'].strip()
                or item.get('status') not in STATUSES or item.get('kind') not in KINDS
                or item.get('verification') not in VERIFICATIONS
                or not isinstance(item.get('lines'), list) or not item['lines']
                or len(set(item['lines'])) != len(item['lines'])
                or any(line not in registry for line in item['lines'])
                or not isinstance(item.get('sources'), list) or not item['sources']):
            raise ValueError('Invalid specimen: ' + ident)
        seen.add(ident)
        date.fromisoformat(item['reviewed_at'])
        if item.get('version') is not None and (not isinstance(item['version'], str) or not item['version'].strip()):
            raise ValueError('Invalid specimen version: ' + ident)
        if any(not isinstance(item.get('summary', {}).get(lang), str) or not item['summary'][lang].strip()
               for lang in ('en', 'ru', 'es', 'zh')):
            raise ValueError('Missing specimen translation: ' + ident)
        missing = item.get('missing')
        if (not isinstance(missing, list) or len(set(missing)) != len(missing)
                or any(key not in MISSING for key in missing)):
            raise ValueError('Invalid specimen gaps: ' + ident)
        if item['status'] in ('pending', 'partial') and not missing:
            raise ValueError('Unfinished specimen needs explicit gaps: ' + ident)
        artifacts = []
        for ref in item.get('artifact_refs', []):
            anchor = anchors.get(ref.get('attribution'))
            artifact = next((a for a in anchor['artifacts'] if a['title'] == ref.get('title')), None) if anchor else None
            if artifact is None:
                raise ValueError('Unknown specimen artifact: ' + ident)
            artifacts.append(copy.deepcopy(artifact))
        if item['verification'] == 'reproduced' and (not artifacts or any(not a.get('sha256') for a in artifacts)):
            raise ValueError('Checked specimen needs pinned, hashed artifacts: ' + ident)
        for file in item.get('files', []):
            name = file.get('name', '')
            if (not re.fullmatch('[A-Za-z0-9_./-]+', name) or name.startswith('/')
                    or any(part in ('', '..') for part in name.split('/'))
                    or not re.fullmatch('[a-f0-9]{64}', file.get('sha256', ''))):
                raise ValueError('Invalid specimen file: ' + ident)
        item['artifacts'] = artifacts
    return catalog


def render_specimens(catalog):
    out = ['# Research specimens', '',
           'Inspected firmware, source trees, bounded negative results and reported leads.',
           'Related atlas lines identify the research question. Partial, negative and pending',
           'records do not assign a device to a measured fleet.', '',
           'Reviewed: **' + catalog['reviewed_at'] + '**. ' + str(len(catalog['items'])) + ' records.', '',
           '[Browse in the atlas](https://scadastrangelove.github.io/TRON-069/#lang=en&tab=wanted)', '',
           '<!-- Generated from data/research-specimens.json by tools/build-map.py. -->', '',
           '| Sample | Material | Result | Verification |', '| --- | --- | --- | --- |']
    for item in catalog['items']:
        out.append('| [' + item['title'] + '](#' + item['id'] + ') | ' + KINDS[item['kind']] + ' | '
                   + STATUSES[item['status']] + ' | ' + VERIFICATIONS[item['verification']] + ' |')
    for item in catalog['items']:
        out += ['', '<a id="' + item['id'] + '"></a>', '## ' + item['title'], '', item['summary']['en'], '',
                'Result: **' + STATUSES[item['status']] + '**. Evidence: ' + VERIFICATIONS[item['verification']] + '.', '',
                'Related research: ' + ', '.join('`' + line + '`' for line in item['lines']) + '.']
        if item.get('version'):
            out += ['', 'Version: `' + item['version'] + '`.']
        for artifact in item['artifacts']:
            out += ['', '- [' + artifact['title'] + '](' + artifact['url'] + ') — SHA-256 `' + artifact['sha256'] + '`.']
        for file in item.get('files', []):
            out += ['', '- Extracted `' + file['name'] + '` — SHA-256 `' + file['sha256'] + '`.']
        if item['missing']:
            out += ['', 'Still needed: ' + ', '.join(MISSING[key] for key in item['missing']) + '.']
        out += ['', 'Research: ' + ' · '.join('[' + s['file'] + '](' + s['file']
                   + ('#' + s['anchor'] if s.get('anchor') else '') + ')' for s in item['sources']) + '.']
    return '\n'.join(out) + '\n'
