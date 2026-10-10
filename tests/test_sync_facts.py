"""Offline checks for promoting complete snapshot counts to current facts."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'tools'))
from collection_catalog import collected_facts, sync_facts
from shodan_count import read, save


class FactSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.path = self.root/'facts.json'
        self.snapshot = self.root/'snapshot-20261010-100000'
        self.facts = {'line': [dict(label='Edited during collection', note='Research count was 99',
                                   dork='all', count=99),
                               dict(label='Subset', note='', dork='subset', count=7)]}
        self.manifest = dict(status='complete', errors=0, plan=dict(id='run', mode='full',
            source_snapshot=None, options={}, facts={'line': [dict(label='Old frozen prose')]},
            base_jobs=[dict(id='line', query='all')], queries=[dict(id='subset', query='subset')]))
        save(self.path, self.facts)
        save(self.snapshot/'manifest.json', self.manifest)
        for file, query, total in [('line.json', 'all', 100), ('variants/subset.json', 'subset', 0)]:
            save(self.snapshot/file, dict(dork=query, total=total, taken='2026-10-10T10:01:00+00:00',
                                         run_id='run', collection_status='ok'))

    def tearDown(self):
        self.temp.cleanup()

    def test_sync_preserves_prose_original_counts_and_snapshot_bytes(self):
        before = {p: p.read_bytes() for p in self.snapshot.rglob('*.json')}
        self.assertEqual(sync_facts(self.path, self.snapshot), 2)
        facts = read(self.path)['line']
        self.assertEqual([f['count'] for f in facts], [100, 0])
        self.assertEqual([f['historical_count'] for f in facts], [99, 7])
        self.assertEqual(facts[0]['label'], self.facts['line'][0]['label'])
        self.assertEqual(facts[0]['note'], self.facts['line'][0]['note'])
        self.assertEqual(facts[1]['collection_source'], dict(snapshot=self.snapshot.name,
            file='variants/subset.json', run_id='run'))
        self.assertEqual(before, {p: p.read_bytes() for p in self.snapshot.rglob('*.json')})
        with patch('shodan_count.save', side_effect=AssertionError('identical sync must not write')):
            self.assertEqual(sync_facts(self.path, self.snapshot), 2)
        rec = read(self.snapshot/'line.json')
        rec.update(total=120, taken='2026-10-11T10:00:00+00:00')
        save(self.snapshot/'line.json', rec)
        sync_facts(self.path, self.snapshot)
        self.assertEqual(read(self.path)['line'][0]['historical_count'], 99)

    def test_bad_last_result_never_partially_updates_source(self):
        path = self.snapshot/'variants/subset.json'
        record = read(path)
        before = self.path.read_bytes()
        for bad in (None, dict(record, dork='wrong query'), dict(record, run_id='old-run'),
                    dict(record, collection_status='error'), dict(record, total=-1),
                    dict(record, taken=None), dict(record, taken='2026-10-10T10:00:00')):
            with self.subTest(record=bad):
                save(path, bad)
                with self.assertRaises(ValueError):
                    sync_facts(self.path, self.snapshot)
                self.assertEqual(self.path.read_bytes(), before)

    def test_new_uncollected_note_is_preserved_and_blocks_promotion(self):
        self.facts['line'].append(dict(label='New research', dork='not in frozen plan', count=3))
        save(self.path, self.facts)
        before = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'Uncollected facts queries'):
            sync_facts(self.path, self.snapshot)
        self.assertEqual(self.path.read_bytes(), before)

    def test_newer_facts_cannot_be_rolled_back(self):
        self.facts['line'][1]['taken'] = '2026-10-11T10:00:00+00:00'
        save(self.path, self.facts)
        before = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'roll back'):
            sync_facts(self.path, self.snapshot)
        self.assertEqual(self.path.read_bytes(), before)

    def test_partial_scoped_inherited_and_custom_runs_do_not_promote(self):
        before = self.path.read_bytes()
        bad = [dict(self.manifest, status='incomplete'), dict(self.manifest, errors=1)]
        for change in (dict(mode='queries-only'), dict(source_snapshot='older'), dict(facts=None),
                       dict(options={'only': ['line']}), dict(options={'query_group': ['subset']}),
                       dict(options={'skip_variants': True})):
            manifest = copy.deepcopy(self.manifest)
            manifest['plan'].update(change)
            bad.append(manifest)
        for manifest in bad:
            with self.subTest(manifest=manifest):
                save(self.snapshot/'manifest.json', manifest)
                with self.assertRaisesRegex(ValueError, 'fresh full collection'):
                    sync_facts(self.path, self.snapshot)
                self.assertEqual(self.path.read_bytes(), before)

    def test_historical_build_keeps_original_count_without_stale_provenance(self):
        sync_facts(self.path, self.snapshot)
        source = read(self.path)
        result = collected_facts(source, self.snapshot, lambda path: None)['line'][0]
        self.assertIsNone(result['count'])
        self.assertEqual(result['historical_count'], 99)
        self.assertNotIn('collection_source', result)
        self.assertEqual(source['line'][0]['count'], 100)


if __name__ == '__main__':
    unittest.main()
