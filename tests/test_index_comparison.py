"""Keep independent FOFA research separate from reproducible Shodan counts."""
import copy
import csv
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from index_comparison import read_comparison

spec = importlib.util.spec_from_file_location('build_map', ROOT/'tools/build-map.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        with (ROOT/'registry.csv').open(newline='') as stream:
            self.registry = {r['id']: r for r in csv.DictReader(stream)}
        self.path = ROOT/'data/index-comparison.json'
        self.data = json.loads(self.path.read_text())

    def changed(self, change):
        data = copy.deepcopy(self.data)
        change(data)
        original = Path.read_text
        def read(path, *args, **kwargs):
            return json.dumps(data) if path == self.path else original(path, *args, **kwargs)
        with patch.object(Path, 'read_text', read):
            return read_comparison(ROOT, self.registry)

    def test_fixed_reference(self):
        data = read_comparison(ROOT, self.registry)
        self.assertEqual(len(data['signatures']), 13)
        self.assertEqual(len(data['countries']), 22)
        self.assertEqual(data['reference_snapshot'], '20261013-160503')

    def test_rejects_mismatched_count_query_and_date(self):
        for field, value in [('shodan_count', 1), ('shodan_query', 'port:80'),
                             ('shodan_taken', '2026-10-15T00:00:00+00:00')]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.changed(lambda d: d['signatures'][0].update({field: value}))

    def test_rejects_invalid_counts_and_private_fields(self):
        for value in [-1, True, None, 1.5]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.changed(lambda d: d['signatures'][0].update(fofa_count=value))
        with self.assertRaises(ValueError):
            self.changed(lambda d: d['countries'][0].update(host='private-record'))

    def test_rejects_duplicate_and_wrong_country_scope(self):
        for change in [lambda d: d['countries'].append(d['countries'][0]),
                       lambda d: d['countries'][0].update(port=8085),
                       lambda d: d['countries'][0].update(shodan_count=0)]:
            with self.assertRaises(ValueError):
                self.changed(change)

    def test_snapshot_independence_and_measurement_integrity(self):
        for ident in ('20261008-2227', '20261013-160503'):
            snapshot = ROOT/'data/mapdata'/('snapshot-'+ident)
            data = builder.build_data(snapshot)
            self.assertEqual(data['comparison'], self.data)
            self.assertNotIn('comparison', builder.SNAPSHOT_FIELDS)
            expected = {}
            for slug, line in data['lines'].items():
                record = json.loads((snapshot/(slug+'.json')).read_text())
                self.assertEqual(line['total'], record['total'])
                self.assertEqual(line['dork'], record['dork'])
                if slug not in data['excluded']:
                    for cc, n in line['countries'].items():
                        expected[cc] = expected.get(cc, 0) + n
            self.assertEqual(data['ident'], expected)
            self.assertEqual(data['lines']['dt-speedport-sdk']['name'], 'DSLForum CPE Management')


if __name__ == '__main__':
    unittest.main()
