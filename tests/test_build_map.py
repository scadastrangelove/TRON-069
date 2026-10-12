"""Offline build regression checks. Never runs the Shodan collector."""
import copy
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('build_map', ROOT/'tools/build-map.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
SNAPSHOT = ROOT/'data/mapdata/snapshot-20261008-2227'


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def snapshot(self):
        target = self.root/SNAPSHOT.name
        shutil.copytree(SNAPSHOT, target)
        return target

    def test_reproducible_from_unrelated_working_directory(self):
        subprocess.run(['python3', str(ROOT/'tools/build-map.py'), '--output-dir', str(self.root)],
                       cwd=self.root, check=True, capture_output=True)
        expected = (ROOT/'index.html').read_bytes()
        self.assertEqual((self.root/'index.html').read_bytes(), expected)
        self.assertEqual((self.root/'atlas/tr-atlas.html').read_bytes(), expected)
        self.assertEqual((ROOT/'atlas/tr-atlas.html').read_bytes(), expected)

    def test_missing_line_rejected_without_publishing(self):
        snapshot = self.snapshot()
        (snapshot/'cpe-server-1-0.json').unlink()
        with self.assertRaisesRegex(ValueError, 'differ from manifest'):
            builder.build(snapshot, self.root/'output')
        self.assertFalse((self.root/'output/index.html').exists())

    def test_failed_manifest_rejected(self):
        snapshot = self.snapshot()
        manifest = builder.read(snapshot/'manifest.json')
        manifest['errors'] = ['API timeout']
        (snapshot/'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'incomplete snapshot'):
            builder.build(snapshot, self.root/'output')

    def test_unknown_fact_line_rejected_without_publishing(self):
        snapshot = self.snapshot()
        original_read = builder.read
        def read_with_typo(path):
            value = original_read(path)
            if path == ROOT/'data/mapdata/facts.json':
                value['cwmp-server-new'] = [{'label': 'Orphaned observation'}]
            return value
        with patch.object(builder, 'read', side_effect=read_with_typo):
            with self.assertRaisesRegex(ValueError, 'Unknown fact line IDs.*cwmp-server-new'):
                builder.build(snapshot, self.root/'output')
        self.assertFalse((self.root/'output/index.html').exists())

    def test_failed_denominator_rejected(self):
        snapshot = self.snapshot()
        record = builder.read(snapshot/'denominator-http.json')
        record['collection_status'] = 'error'
        (snapshot/'denominator-http.json').write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'Incomplete denominator'):
            builder.build(snapshot, self.root/'output')

    def test_missing_editorial_translation_rejected(self):
        data = dict(meta=builder.read(ROOT/'data/mapmeta.json'),
                    facts=builder.read(ROOT/'data/mapdata/facts.json'),
                    orgnorm=builder.read(ROOT/'data/orgnorm.json'),
                    translations=builder.read(ROOT/'data/content-i18n.json'))
        builder.validate_translations(data)
        missing = copy.deepcopy(data)
        missing['meta']['lines']['cpe-server-1-0']['findings'].append('Новая заметка без перевода')
        with self.assertRaisesRegex(ValueError, 'Missing content translations'):
            builder.validate_translations(missing)

    def test_ui_translation_keys_match(self):
        ui = builder.read(ROOT/'data/ui-i18n.json')
        for lang in ('ru', 'es', 'zh'):
            self.assertEqual(set(ui['en']), set(ui[lang]), lang)

    def test_ecosystem_rejects_broken_and_non_public_evidence(self):
        with (ROOT/'registry.csv').open() as stream:
            registry = {row['id']: row for row in csv.DictReader(stream)}
        catalog = builder.read_ecosystem(registry)
        def check_bad(change, message):
            bad = copy.deepcopy(catalog)
            change(bad)
            original_read = builder.read
            with patch.object(builder, 'read', side_effect=lambda path: bad if path.name == 'acs-relations.json' else original_read(path)):
                with self.assertRaisesRegex(ValueError, message):
                    builder.read_ecosystem(registry)
        check_bad(lambda c: c['edges'][0].update(target='missing'), 'Dangling')
        check_bad(lambda c: c['edges'][0]['summary'].pop('zh'), 'translation')
        check_bad(lambda c: c['nodes'].append(c['nodes'][0]), 'duplicate')
        check_bad(lambda c: c['nodes'][0].update(line='genieacs-admin-ui'), 'registry role')
        check_bad(lambda c: c['edges'][0].update(sources=[{'url':'https://user:secret@example.org', 'title':'bad'}]), 'URL')
        check_bad(lambda c: c['edges'][0].update(sources=[{'file':'private/report.md'}]), 'Non-public')
        check_bad(lambda c: c['edges'][0].update(sources=[{'file':'../report.md'}]), 'Non-public')
        check_bad(lambda c: c['edges'][0].update(sources=[]), 'Missing ecosystem sources')
        check_bad(lambda c: c['edges'][0].update(map={'line':'gateway-realm','country':'IT'}), 'map scope')
        check_bad(lambda c: c['edges'][0].update(credentials='secret'), 'Unknown ecosystem edge fields')

    def test_operator_aliases_require_unambiguous_country_scopes(self):
        catalog = builder.read_operators()
        def check_bad(change, message):
            bad = copy.deepcopy(catalog)
            change(bad)
            with patch.object(builder, 'read', return_value=bad):
                with self.assertRaisesRegex(ValueError, message):
                    builder.read_operators()
        check_bad(lambda c: c['operators'][0]['aliases'].append(' TPG INTERNET PTY LTD '), 'Ambiguous')
        check_bad(lambda c: c['operators'][0].update(group='absent'), 'Unknown operator group')
        check_bad(lambda c: c['groups'][0]['source'].update(url='https://user:secret@example.org'), 'source')
        check_bad(lambda c: c['operators'].append(c['operators'][0]), 'duplicate')
        other = copy.deepcopy(catalog['operators'][0])
        other.update(id='other-country', country='GB')
        catalog['operators'].append(other)
        with patch.object(builder, 'read', return_value=catalog):
            self.assertEqual(builder.read_operators(), catalog)

    def test_ecosystem_sources_are_checked_and_old_snapshots_keep_evidence_dates(self):
        data = builder.build(SNAPSHOT, self.root/'output')
        self.assertEqual(data['ecosystem'], builder.read(ROOT/'data/acs-relations.json'))
        edge = next(e for e in data['ecosystem']['edges'] if e['id']=='mifibra-zte-deployment')
        self.assertEqual(edge['observed'], '2024-12-20')
        data['ecosystem']['edges'][0]['sources'] = [{'file':'missing-public-source.md'}]
        with self.assertRaisesRegex(ValueError, 'Invalid public source reference'):
            builder.validate_sources(data)

    def test_fact_counts_are_read_from_exact_dated_records(self):
        facts={'line':[dict(dork='"line"',count=999,collection_ref=dict(kind='variant',id='slice'))]}
        rec=dict(dork='"line"',total=0,taken='2026-10-10T10:00:00+00:00',collection_status='ok')
        fresh=builder.collected_facts(facts,self.root,lambda path:rec)
        self.assertEqual(fresh['line'][0]['count'],0)
        self.assertEqual(fresh['line'][0]['taken'],rec['taken'])
        self.assertEqual(fresh['line'][0]['historical_count'],999)
        wrong=builder.collected_facts(facts,self.root,lambda path:dict(rec,dork='different'))
        self.assertIsNone(wrong['line'][0]['count'])
        missing=builder.collected_facts(facts,self.root,lambda path:None)
        self.assertIsNone(missing['line'][0]['count'])
        self.assertEqual(facts['line'][0]['count'],999)

    def test_history_does_not_promote_partial_or_failed_snapshots(self):
        for ident,status,errors in [('20261008-000000','complete',0),('20261009-000000','complete',1),('20261010-000000','running',0)]:
            path=self.root/f'snapshot-{ident}'
            path.mkdir()
            (path/'manifest.json').write_text(json.dumps(dict(status=status,errors=errors,lines=[])))
        history=builder.snapshot_history(self.root)
        self.assertEqual(history['latest_complete'],'snapshot-20261008-000000')
        self.assertEqual(len(history['snapshots']),3)

    def test_paused_collection_cannot_publish(self):
        snapshot = self.snapshot()
        manifest = builder.read(snapshot/'manifest.json')
        manifest['status'] = 'paused'
        (snapshot/'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'incomplete snapshot checkpoint'):
            builder.build(snapshot, self.root/'output')
        self.assertFalse((self.root/'output/index.html').exists())

    def test_news_requires_translations_and_evidence(self):
        news = builder.read_news()
        missing = copy.deepcopy(news)
        del missing[0]['body']['zh']
        with patch.object(builder, 'read', return_value=missing):
            with self.assertRaisesRegex(ValueError, 'Missing news translation'):
                builder.read_news()
        missing = copy.deepcopy(news)
        missing[0]['evidence'] = []
        with patch.object(builder, 'read', return_value=missing):
            with self.assertRaisesRegex(ValueError, 'Missing news evidence'):
                builder.read_news()

    def test_missing_or_escaping_source_reference_rejected(self):
        data = dict(meta={'lines':{}},facts={},variants={},news=[])
        for name in ('missing-research.md', '../outside.md', '/etc/passwd'):
            data['meta']['lines']={'line':{'sources':[{'file':name}]}}
            with self.assertRaisesRegex(ValueError,'Invalid public source'):
                builder.validate_sources(data)
        data['meta']['lines']={'line':{'sources':[{'file':'README.md','anchor':'missing-anchor'}]}}
        with self.assertRaisesRegex(ValueError,'Missing public source anchor'):
            builder.validate_sources(data)

    def test_manifesto_stays_first_when_newer_news_is_added(self):
        news = builder.read_news()
        manifesto = next(item for item in news if item['id'] == 'tron-069-manifesto')
        self.assertTrue(manifesto['pinned'])
        newer = copy.deepcopy(next(item for item in news if not item.get('pinned')))
        newer.update(id='future-news', date='2099-01-01')
        # Reorder the input too: neither its position nor its date should pin it.
        with patch.object(builder, 'read', return_value=[newer, *reversed(news)]):
            ordered = builder.read_news()
        self.assertEqual(ordered[0]['id'], manifesto['id'])
        self.assertEqual(ordered[1]['id'], 'future-news')
        dates = [item['date'] for item in ordered[1:]]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_news_pin_and_external_links_are_validated(self):
        news = builder.read_news()
        for pinned, message in [('true', 'must be boolean'), (True, 'Only one')]:
            invalid = copy.deepcopy(news)
            invalid[1]['pinned'] = pinned
            with patch.object(builder, 'read', return_value=invalid):
                with self.assertRaisesRegex(ValueError, message):
                    builder.read_news()
        for url in ('javascript:alert(1)', '//example.com', 'https://user:secret@example.com', 'https://example.com/a b'):
            invalid = copy.deepcopy(news)
            invalid[0]['links'] = [{'label':'Example','url':url}]
            with patch.object(builder, 'read', return_value=invalid):
                with self.assertRaisesRegex(ValueError, 'Invalid news link'):
                    builder.read_news()

    def test_acs_is_excluded_independently_of_static_exclusion_list(self):
        snapshot=self.snapshot()
        rec=builder.read(snapshot/'tr069-client.json')
        rec['name']='Telefónica cwmpWeb'
        (snapshot/'telefonica-cwmpweb.json').write_text(json.dumps(rec))
        manifest=builder.read(snapshot/'manifest.json')
        manifest['lines'].append(dict(name=rec['name'],file='telefonica-cwmpweb.json',collection_status='ok'))
        (snapshot/'manifest.json').write_text(json.dumps(manifest))
        data=builder.build(snapshot,self.root/'output')
        self.assertEqual(data['lines']['telefonica-cwmpweb']['service'],'acs')
        self.assertIn('telefonica-cwmpweb',data['excluded'])
        expected=sum(line['countries'].get('US',0) for slug,line in data['lines'].items() if slug not in data['excluded'])
        self.assertEqual(data['ident']['US'],expected)

    def test_missing_planned_variant_blocks_build(self):
        snapshot=self.snapshot()
        manifest=builder.read(snapshot/'manifest.json')
        manifest['plan']=dict(id='run',queries=[dict(id='absent',query='test',facets='org:10')])
        (snapshot/'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError,'planned variant'):
            builder.build(snapshot,self.root/'output')
        self.assertFalse((self.root/'output/index.html').exists())

    def test_variant_shares_require_same_run_denominator(self):
        snapshot=self.snapshot();directory=snapshot/'variants';directory.mkdir()
        base=dict(id='all',parent='avsystem-libcwmp',run_id='a',collection_status='ok',total=100)
        version=dict(id='v',parent='avsystem-libcwmp',run_id='b',collection_status='ok',total=25,denominator='all')
        for item in (base,version):(directory/(item['id']+'.json')).write_text(json.dumps(item))
        items=builder.read_variants(snapshot,{},['avsystem-libcwmp'])['avsystem-libcwmp']
        self.assertIsNone(next(i for i in items if i['id']=='v')['share'])
        version['run_id']='a';(directory/'v.json').write_text(json.dumps(version))
        items=builder.read_variants(snapshot,{},['avsystem-libcwmp'])['avsystem-libcwmp']
        self.assertEqual(next(i for i in items if i['id']=='v')['share'],0.25)


if __name__ == '__main__':
    unittest.main()
