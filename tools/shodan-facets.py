#!/usr/bin/env python3
"""Compatibility entry point for the easycwmp catalog group.

Uses the same Count client, CLI credentials, saved plans and JSON snapshots as
collect-map.py. Default: ten easycwmp aggregate queries, no base or operator sweep.
Resume a stopped run with: shodan-facets.py --resume SNAPSHOT
"""
import importlib.util
from pathlib import Path
import sys

spec = importlib.util.spec_from_file_location('collect_map', Path(__file__).with_name('collect-map.py'))
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)

if __name__ == '__main__':
    flags = sys.argv[1:]
    if '--resume' not in flags and not any(f.startswith('--resume=') for f in flags):
        flags = ['--queries-only', '--query-group', 'easycwmp'] + flags
    sys.exit(collector.main(flags))
