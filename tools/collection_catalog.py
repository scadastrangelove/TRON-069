"""Bind editorial observations to exact, versioned collection queries."""
from copy import deepcopy
from datetime import datetime


def bind_facts(facts, base_jobs, queries, *, strict=True):
    refs = {job['query']: {'kind': 'base', 'id': job['id']} for job in base_jobs}
    refs.update({job['query']: {'kind': 'variant', 'id': job['id']} for job in queries})
    bound = deepcopy(facts)
    missing = []
    for parent, items in bound.items():
        for item in items:
            query = item.get('dork')
            ref = refs.get(query)
            if ref:
                item['collection_ref'] = ref.copy()
            else:
                item.pop('collection_ref', None)
                missing.append(f'{parent}: {query}')
    if strict and missing:
        raise ValueError('Uncollected facts queries; add them to data/collection-queries.json: '+ '; '.join(missing))
    return bound


def collected_facts(facts, snapshot, read):
    """Use dated API results; never silently relabel handwritten counts as fresh."""
    bound = deepcopy(facts)
    for items in bound.values():
        for item in items:
            item.setdefault('historical_count', item.get('count'))
            ref = item.get('collection_ref', {})
            ident = ref.get('id', '')
            if ref.get('kind') not in ('base', 'variant') or not ident or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in ident):
                record = None
            else:
                path = snapshot / ('variants' if ref.get('kind') == 'variant' else '') / (ident+'.json')
                record = read(path)
            valid = bool(record and record.get('collection_status') == 'ok'
                         and record.get('dork') == item['dork']
                         and type(record.get('total')) is int and record['total'] >= 0)
            item['count'] = record['total'] if valid else None
            item['taken'] = record.get('taken') if valid else None
            item['collection_status'] = 'ok' if valid else 'not-collected'
            item.pop('collection_source', None)
            if valid:
                item['collection_source'] = dict(snapshot=snapshot.name,
                    file=path.relative_to(snapshot).as_posix(), run_id=record.get('run_id'))
    return bound


def can_sync_facts(plan):
    """Only fresh, unscoped standard collections can advance the source facts."""
    options = plan.get('options', {})
    return bool(plan.get('mode') == 'full' and not plan.get('source_snapshot')
                and plan.get('facts') is not None
                and not any(options.get(key) for key in ('only', 'query_group', 'skip_variants')))


def dated(value):
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (AttributeError, TypeError, ValueError):
        raise ValueError('Missing or invalid facts collection timestamp') from None
    if result.tzinfo is None:
        raise ValueError('Facts collection timestamp must include a timezone')
    return result


def sync_facts(path, snapshot):
    """Atomically refresh current facts, preserving prose and the original counts.

    Read current editorial data, not the frozen copy: edits made during a long
    collection must survive. Validate every result before changing the source.
    """
    from shodan_count import read, save

    manifest = read(snapshot/'manifest.json') or {}
    plan = manifest.get('plan', {})
    if manifest.get('status') != 'complete' or manifest.get('errors') or not can_sync_facts(plan):
        raise ValueError('Facts sync requires a completed, error-free fresh full collection')
    facts = read(path)
    if not isinstance(facts, dict):
        raise ValueError('Invalid facts source')
    bound = bind_facts(facts, plan['base_jobs'], plan['queries'])
    fresh = collected_facts(bound, snapshot, read)
    count = 0
    for parent, items in fresh.items():
        for old, item in zip(facts[parent], items):
            if (item['collection_status'] != 'ok' or not plan.get('id')
                    or item['collection_source']['run_id'] != plan['id']):
                raise ValueError(f'Missing or mismatched facts result: {parent}: {item["dork"]}')
            taken = dated(item['taken'])
            if old.get('taken') and dated(old['taken']) > taken:
                raise ValueError(f'Refusing to roll back newer facts: {parent}: {item["dork"]}')
            count += 1
    if fresh != facts:
        save(path, fresh)
    return count
