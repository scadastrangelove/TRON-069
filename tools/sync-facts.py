#!/usr/bin/env python3
"""Refresh facts.json from a completed fresh full snapshot without API requests."""
import argparse
from pathlib import Path
from collection_catalog import sync_facts

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot', type=Path)
    args = parser.parse_args()
    try:
        count = sync_facts(ROOT/'data/mapdata/facts.json', args.snapshot.resolve())
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f'Facts unchanged: {exc}\n')
    print(f'Updated facts.json: {count} dated observations')


if __name__ == '__main__':
    main()
