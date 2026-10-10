"""Small index of immutable Shodan collection directories; no credentials or IPs."""
from pathlib import Path
from shodan_count import read, save


def snapshot_history(directory):
    entries = []
    for path in sorted(Path(directory).glob('snapshot-*')):
        manifest = read(path/'manifest.json')
        if not isinstance(manifest, dict):
            continue
        lines = manifest.get('lines', [])
        entries.append(dict(
            snapshot=path.name, status=manifest.get('status', 'complete'),
            started_at=manifest.get('started_at', manifest.get('taken')),
            completed_at=manifest.get('completed_at'), updated_at=manifest.get('updated_at'),
            source_snapshot=manifest.get('source_snapshot'),
            mode=manifest.get('collector_mode', 'legacy'), errors=manifest.get('errors', 0),
            lines=sum(row.get('collection_status') == 'ok' for row in lines
                      if not row['file'].startswith('denominator-')),
            operator_pairs=manifest.get('org_drill', {}),
            research_queries=manifest.get('variants', {}),
        ))
    complete = [item for item in entries if item['status'] == 'complete' and not item['errors']]
    return dict(schema_version=1, timezone='UTC', latest_complete=complete[-1]['snapshot'] if complete else None,
                snapshots=entries)


def write_history(directory):
    history = snapshot_history(directory)
    save(Path(directory)/'history.json', history)
    return history
