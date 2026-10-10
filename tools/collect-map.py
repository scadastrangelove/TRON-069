#!/usr/bin/env python3
"""Collect public Shodan Count aggregates, never host records or active scans.

Default: every registry line × every observed country; top-100 org and ASN
facets per pair. Count does not consume query credits; an API key is required.
https://developer.shodan.io/api#shodan-host-count

--dry-run prints the plan without reading a key or contacting the API.
--from-snapshot DIR preserves history; --resume DIR restores its saved plan.
Catalog queries live in data/collection-queries.json. --only selects stable IDs.
Successful compatible files are reused. Each response and the manifest are saved
atomically. --build regenerates the atlas after the requested collection is complete.
"""
import argparse
import csv
import fcntl
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shodan_count import (CountClient, CountError, RequestBudget, cli_config_dir,
                          load_key, now, read, save, slugify, compatible, facet_meta, country_query)
from collection_catalog import bind_facts, can_sync_facts, sync_facts
from snapshot_history import write_history

ROOT = Path(__file__).resolve().parent.parent
BASE_FACETS = 'country:250,asn:100,port:100'
STICKER_LINES = {
    'genieacs': ('genieacs-admin-ui', 'GenieACS admin-UI'),
    'cwmp_agent': ('cwmp-agent-orange-tunisie', 'CWMP-Agent'),
}


def base_jobs():
    with (ROOT/'registry.csv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    jobs = [(r.get('id') or slugify(r['product']), r['product'], r['shodan_dork'], BASE_FACETS) for r in rows]
    jobs += [('denominator-park', 'denominator-park', 'port:7547', 'country:250'),
             ('denominator-http', 'denominator-http', 'port:7547 HTTP', 'country:250')]
    if any(not re.fullmatch('[a-z0-9-]+', j[0]) for j in jobs):
        raise ValueError('Invalid registry ID')
    if len({j[0] for j in jobs}) != len(jobs):
        raise ValueError('Duplicate registry slug')
    return jobs


def drill_jobs(records, line_limit=0, country_limit=0):
    lines = sorted(((slug, rec) for slug, rec in records.items()
                    if not slug.startswith('denominator-')), key=lambda pair: (-pair[1]['total'], pair[0]))
    if line_limit:
        lines = lines[:line_limit]
    jobs = []
    for slug, rec in lines:
        countries = sorted(rec['countries'], key=lambda c: (-c['count'], c['value']))
        if country_limit:
            countries = countries[:country_limit]
        for country in countries:
            cc = country['value']
            if country['count'] > 0 and re.fullmatch('[A-Z]{2}', cc):
                jobs.append((f'{slug}--{cc}', rec['name'], cc, country_query(rec['dork'], cc)))
    return jobs


PLAN_DEFAULTS = dict(drill_lines=0, drill_countries=0, org_limit=100, asn_limit=100,
                     skip_drill=False, skip_stickers=False, skip_variants=False,
                     queries_only=False, refresh_base=False, only=[], query_group=[])


def catalog_jobs(path=None, parents=None):
    path = path or ROOT/'data/collection-queries.json'
    catalog = read(path)
    if not isinstance(catalog, dict) or catalog.get('schema_version') != 1:
        raise ValueError('Invalid collection query catalog')
    result, ids = [], set()
    for item in catalog['queries']:
        ident = item['id']
        if not re.fullmatch('[a-z0-9-]+', ident) or ident in ids:
            raise ValueError('Invalid or duplicate query ID')
        ids.add(ident)
        if parents is not None and item['parent'] not in parents:
            raise ValueError(f'Unknown query parent: {ident}')
        if not item.get('query') or not re.fullmatch(r'(?:country|org|asn|port):[1-9][0-9]*(?:,(?:country|org|asn|port):[1-9][0-9]*)*', item['facets']):
            raise ValueError(f'Invalid query/facets: {ident}')
        if any(not item['label'].get(lang) for lang in ('ru','en','es','zh')):
            raise ValueError(f'Missing query translation: {ident}')
        evidence = (ROOT/item['source']['file']).resolve()
        if not evidence.is_relative_to(ROOT) or not evidence.is_file():
            raise ValueError(f'Invalid query source: {ident}')
        result.append(item)
    for item in result:
        if item.get('denominator') and item['denominator'] not in ids:
            raise ValueError(f'Unknown denominator: {item["id"]}')
    return result


def csv_list(value):
    return sorted(set(x.strip() for x in value.split(',') if x.strip()))


def fact_plan(jobs, queries):
    return bind_facts(read(ROOT/'data/mapdata/facts.json') or {}, jobs, queries)


def parser():
    ap = argparse.ArgumentParser(description=__doc__)
    source = ap.add_mutually_exclusive_group()
    source.add_argument('--resume', type=Path, help='resume the exact saved plan')
    source.add_argument('--from-snapshot', type=Path, help='copy a completed snapshot into a new directory')
    source.add_argument('--drill-only', type=Path, help='legacy: extend operator data IN PLACE; prefer --from-snapshot')
    ap.add_argument('--output-dir', type=Path, help='new snapshot directory (must not exist)')
    ap.add_argument('--only', type=csv_list, help='comma-separated stable registry IDs; requires --from-snapshot')
    ap.add_argument('--query-group', type=csv_list, help='only these catalog groups')
    ap.add_argument('--query-catalog', type=Path, help='alternative catalog; embedded in saved plan')
    ap.add_argument('--drill-lines', type=int, help='0 = all selected lines (default)')
    ap.add_argument('--drill-countries', type=int, help='0 = all countries per selected line (default)')
    ap.add_argument('--org-limit', type=int, help='org facet size, default 100')
    ap.add_argument('--asn-limit', type=int, help='ASN facet size, default 100')
    ap.add_argument('--interval', type=float, help='minimum seconds between requests (>=1; default 1.1)')
    ap.add_argument('--shodan-config-dir', type=Path)
    ap.add_argument('--max-requests', type=int, help='stop at this number of HTTP attempts; resume later')
    for flag in ('skip-drill','skip-stickers','skip-variants','queries-only','refresh-base'):
        ap.add_argument('--'+flag, action='store_true', default=None)
    ap.add_argument('--dry-run', action='store_true', help='no key, network access or writes')
    ap.add_argument('--build', action='store_true')
    return ap


def usable(record, query):
    return bool(record and record.get('collection_status') == 'ok' and record.get('dork') == query)


def prepare(args):
    if args.output_dir and (args.resume or args.drill_only):
        raise ValueError('--output-dir cannot be used with an in-place resume')
    ts = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    parent = ROOT/('data/research' if args.queries_only and not args.from_snapshot else 'data/mapdata')
    out = (args.resume or args.drill_only or args.output_dir or parent/f'snapshot-{ts}').resolve()
    if args.resume:
        manifest = read(out/'manifest.json') or {}
        plan = manifest.get('plan')
        if not plan:
            raise ValueError('Checkpoint has no saved plan; start a new collection')
        for key in PLAN_DEFAULTS:
            supplied = getattr(args, key)
            if supplied is not None and supplied != plan['options'][key]:
                raise ValueError(f'--{key.replace("_", "-")} conflicts with the saved plan')
        if args.query_catalog:
            raise ValueError('Resume uses the catalog embedded in its saved plan')
        return out, out, plan, manifest
    if out.exists() and not args.drill_only:
        raise ValueError('Output exists; use --resume to continue it')
    source = args.from_snapshot or args.drill_only
    source = source.resolve() if source else None
    old = read(source/'manifest.json') if source else {}
    if source and (not source.is_dir() or not old):
        raise ValueError('Source snapshot/manifest does not exist')
    if source and (old.get('status','complete') != 'complete' or old.get('errors')):
        raise ValueError('Source snapshot must be complete; resume its saved plan first')
    if args.from_snapshot and (out == source or out.is_relative_to(source)):
        raise ValueError('Output must be outside the source snapshot')
    options = {k: getattr(args,k) if getattr(args,k) is not None else v for k,v in PLAN_DEFAULTS.items()}
    if options['only'] and not source and not options['queries_only']:
        raise ValueError('--only requires --from-snapshot to preserve the other lines')
    if args.drill_only and (options['skip_drill'] or options['queries_only'] or options['refresh_base']):
        raise ValueError('Operator-only collection flags are incompatible')
    if args.drill_only:
        options.update(skip_variants=True, skip_stickers=True)
    jobs = [dict(id=s, name=n, query=q, facets=f) for s,n,q,f in base_jobs()]
    parents = {j['id'] for j in jobs if not j['id'].startswith('denominator-')}
    selected = set(options['only']) or parents
    if selected - parents:
        raise ValueError(f'Unknown line IDs: {sorted(selected-parents)}')
    variants = [] if options['skip_variants'] else catalog_jobs(args.query_catalog, parents)
    facts = fact_plan(jobs, variants) if not options['skip_variants'] and not args.query_catalog else None
    groups = set(options['query_group'])
    if groups - {v['group'] for v in variants}:
        raise ValueError('Unknown query group')
    variants = [v for v in variants if v['parent'] in selected and (not groups or v['group'] in groups)]
    # Include denominator queries even if a future catalog places them in another group.
    chosen = {v['id']:v for v in variants}
    if variants:
        all_variants = {v['id']:v for v in catalog_jobs(args.query_catalog, parents)}
        pending = list(chosen.values())
        while pending:
            denominator = pending.pop().get('denominator')
            if denominator and denominator not in chosen:
                chosen[denominator] = all_variants[denominator]
                pending.append(chosen[denominator])
    if options['queries_only']:
        jobs = [] if not source else jobs
        options.update(skip_drill=True, skip_stickers=True)
    source_ref = (str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else source.name) if source else None
    plan = dict(version=1, id=str(uuid.uuid4()), snapshot_time=ts, created_at=now(), source_snapshot=source_ref,
                mode='drill-only' if args.drill_only else 'queries-only' if options['queries_only'] else 'full',
                options=options, selected=sorted(selected), base_jobs=jobs, queries=list(chosen.values()),
                interval=args.interval or 1.1, facts=facts)
    return out, source, plan, old or {}


def collect(args, client_factory=CountClient):
    out, source, plan, old_manifest = prepare(args)
    if args.resume and old_manifest.get('status') == 'complete' and not args.dry_run:
        print(f'Already complete; preserved unchanged: {out}', flush=True)
        if args.build:
            return subprocess.run([sys.executable,str(ROOT/'tools/build-map.py'),str(out)],check=False).returncode
        return 0
    opt = plan['options']
    for key in ('drill_lines','drill_countries','org_limit','asn_limit'):
        if opt[key] < (1 if key.endswith('limit') else 0):
            raise ValueError('Invalid collection limits')
    interval = args.interval if args.interval is not None else plan['interval']
    if not 1 <= interval < float('inf'):
        raise ValueError('--interval must be finite and at least 1 second')
    if args.max_requests is not None and args.max_requests < 1:
        raise ValueError('--max-requests must be positive')
    if args.build and not plan['base_jobs']:
        raise ValueError('--build needs a full atlas base; use --from-snapshot')
    records = {}
    for job in plan['base_jobs']:
        slug, q = job['id'], job['query']
        rec = read(source/f'{slug}.json') if source else None
        valid = usable(rec, q)
        selected = slug in plan['selected']
        force = plan['mode']=='full' and (opt['refresh_base'] or bool(opt['only'])) and selected
        if force and (not rec or rec.get('run_id') != plan['id']):
            valid = False
        if plan['mode']=='drill-only' or opt['queries_only'] or (opt['only'] and not selected):
            if not valid:
                raise ValueError(f'Missing or outdated preserved base: {slug}')
        elif not source:
            valid = False
        if valid:
            records[slug] = rec
    def pair_plan():
        subset = {s:r for s,r in records.items() if s in plan['selected']}
        return [] if opt['skip_drill'] else drill_jobs(subset, opt['drill_lines'], opt['drill_countries'])
    pairs = pair_plan()
    facets = f'org:{opt["org_limit"]},asn:{opt["asn_limit"]}'
    cached = sum(compatible(read(source/'org-drill'/f'{s}.json'),q,facets) for s,_,_,q in pairs) if source else 0
    query_jobs = plan['queries']
    def query_cached(base, job):
        rec = read(base/'variants'/f'{job["id"]}.json') if base else None
        return bool(compatible(rec,job['query'],job['facets']) and rec.get('run_id')==plan['id'])
    if args.dry_run:
        print(json.dumps(dict(output=str(out), source=str(source) if source else None,
            base_requests=len(plan['base_jobs'])-len(records), selected_lines=plan['selected'],
            pair_requests=len(pairs)-cached if len(records)==len(plan['base_jobs']) else 'determined after country facets',
            selected_pairs=len(pairs), reusable_pairs=cached,
            variant_requests=sum(not query_cached(source,q) for q in query_jobs),
            fact_observations=sum(map(len, (plan.get('facts') or {}).values())),
            sticker_requests=int(not opt['skip_stickers'] and plan['mode']=='full'),
            requested_facets=facets, interval_seconds=interval, query_credits=0,
            scope='selected lines' if opt['only'] else 'all lines', plan_frozen=bool(args.resume)),ensure_ascii=False,indent=2))
        return 0
    key = load_key(args.shodan_config_dir)
    if source and source != out:
        # Copy only validated snapshot data, never links or arbitrary adjacent files.
        out.mkdir(parents=True)
        allowed = {j['id']+'.json' for j in plan['base_jobs']} | {'stickers.json'}
        for name in allowed:
            path = source/name
            if path.is_symlink():
                raise ValueError('Symlinks are not snapshot data')
            if path.is_file():
                shutil.copy2(path,out/name)
        for subdir in ('org-drill','variants'):
            for path in (source/subdir).glob('*.json'):
                if path.is_symlink():
                    raise ValueError('Symlinks are not snapshot data')
                (out/subdir).mkdir(exist_ok=True)
                shutil.copy2(path,out/subdir/path.name)
    else:
        out.mkdir(parents=True,exist_ok=bool(source))
    client = client_factory(key,interval=interval,max_requests=args.max_requests)
    failures = {}
    snapshot_time = plan.get('snapshot_time',plan['id'])
    manifest = dict(taken=old_manifest.get('taken',snapshot_time) if out==source else snapshot_time,
                    started_at=old_manifest.get('started_at',now()) if args.resume else now(),
                    source='Shodan /shodan/host/count', timezone='UTC', plan=plan,
                    source_snapshot=plan['source_snapshot'], collector_mode=plan['mode'])
    completed = set()
    def checkpoint(status='running'):
        done_queries=sum(query_cached(out,q) for q in query_jobs)
        manifest.update(status=status,updated_at=now(),requests_this_run=client.requests,
            errors=len(failures),failures=failures,
            lines=[dict(name=j['name'],file=j['id']+'.json',collection_status='ok' if j['id'] in records else 'pending',
                       **({'total':records[j['id']]['total']} if j['id'] in records else {})) for j in plan['base_jobs']],
            org_drill=dict(scope='skipped' if opt['skip_drill'] else 'selected' if opt['only'] else 'limited' if opt['drill_lines'] or opt['drill_countries'] else 'all',
                expected=len(pairs),completed=len(completed),pending=len(pairs)-len(completed),
                org_limit=opt['org_limit'],asn_limit=opt['asn_limit']),
            variants=dict(expected=len(query_jobs),completed=done_queries,pending=len(query_jobs)-done_queries))
        if status == 'complete':
            manifest['completed_at'] = now()
        save(out/'manifest.json',manifest)
    checkpoint()
    def request(q,f,ident):
        try:
            return client.count(q,f)
        except CountError as exc:
            failures[ident]=str(exc);checkpoint()
            print(f'ERROR {ident}: {exc}',flush=True)
            if exc.fatal:raise
            return None
    def record(data,q,f):
        groups=data.get('facets',{})
        return dict(dork=q,total=data['total'],taken=now(),run_id=plan['id'],collection_status='ok',
                    requested_facets=f,facet_meta={k:facet_meta(groups.get(k,[]),data['total']) for k in requested_keys(f)},
                    countries=groups.get('country',[]),asn=groups.get('asn',[]),ports=groups.get('port',[]),orgs=groups.get('org',[]))
    try:
        for job in plan['base_jobs']:
            slug=job['id']
            if slug in records:continue
            data=request(job['query'],job['facets'],slug)
            if data is not None:
                rec=record(data,job['query'],job['facets']);rec['name']=job['name']
                save(out/f'{slug}.json',rec);records[slug]=rec
                # Refreshed base can have a different set of countries; discard old slices in this output only.
                for path in (out/'org-drill').glob(f'{slug}--*.json'):path.unlink()
            checkpoint()
            print(f'Base {len(records)}/{len(plan["base_jobs"])}: {slug}',flush=True)
        if len(records)!=len(plan['base_jobs']):
            checkpoint('incomplete');return 1
        pairs=pair_plan();checkpoint()
        for i,(slug,name,cc,q) in enumerate(pairs,1):
            path=out/'org-drill'/f'{slug}.json'
            if not compatible(read(path),q,facets):
                data=request(q,facets,slug)
                if data is not None:
                    rec=record(data,q,facets);rec.update(line=name,line_id=slug.rsplit('--',1)[0],cc=cc)
                    save(path,rec)
            if compatible(read(path),q,facets):completed.add(slug)
            checkpoint()
            print(f'Pairs {i}/{len(pairs)}: {slug}',flush=True)
        for job in query_jobs:
            if query_cached(out,job):continue
            data=request(job['query'],job['facets'],job['id'])
            if data is not None:
                rec=record(data,job['query'],job['facets'])
                rec.update({k:job[k] for k in ('id','parent','group','label','source')})
                rec['denominator']=job.get('denominator')
                save(out/'variants'/f'{job["id"]}.json',rec)
            checkpoint()
            print(f'Variant: {job["id"]}',flush=True)
        if not opt['skip_stickers'] and plan['mode']=='full':
            stickers=read(out/'stickers.json') or {}
            q,f='port:7547 ssl','country:250,asn:10'
            if not compatible(stickers.get('tls_cr'),q,f):
                data=request(q,f,'sticker-tls')
                if data is not None:
                    stickers['tls_cr']=record(data,q,f);stickers['tls_cr']['label']='TLS on CR port'
            for key,(slug,label) in STICKER_LINES.items():
                if slug in records:
                    rec=records[slug]
                    stickers[key]=dict(label=label,query=rec['dork'],total=rec['total'],taken=rec['taken'],countries=rec['countries'])
            save(out/'stickers.json',stickers)
        checkpoint('incomplete' if failures else 'complete')
    except RequestBudget:
        checkpoint('paused');print(f'Request limit reached. Resume: --resume {out}',flush=True);return 3
    except CountError:
        checkpoint('incomplete');return 1
    except KeyboardInterrupt:
        checkpoint('interrupted');print(f'Interrupted. Resume: --resume {out}',flush=True);return 130
    print(f'Saved {out}; pairs {len(completed)}/{len(pairs)}; variants {manifest["variants"]["completed"]}/{len(query_jobs)}; errors {len(failures)}',flush=True)
    if failures:return 1
    if can_sync_facts(plan):
        count = sync_facts(ROOT/'data/mapdata/facts.json', out)
        print(f'Updated facts.json: {count} dated observations', flush=True)
    if args.build:
        return subprocess.run([sys.executable,str(ROOT/'tools/build-map.py'),str(out)],check=False).returncode
    return 0


def requested_keys(facets):
    return [field.split(':')[0] for field in facets.split(',')]


def main(argv=None):
    args=parser().parse_args(argv)
    try:
        if args.dry_run:
            return collect(args)
        # One collector per checkout prevents daily/manual runs from competing
        # for the API and prevents concurrent writes to a resumed checkpoint.
        lock_path = ROOT/'data/.collection.lock'
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open('a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise ValueError('Another collector is running in this checkout') from None
            try:
                return collect(args)
            finally:
                write_history(ROOT/'data/mapdata')
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(f'Collection stopped: {exc}',file=sys.stderr)
        return 1


if __name__=='__main__':sys.exit(main())
