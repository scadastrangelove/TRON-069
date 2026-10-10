"""Offline regression tests for the Count collector; all HTTP is stubbed."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('collector', ROOT/'tools/collect-map.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def response(total=10, facets=None):
    return io.BytesIO(json.dumps(dict(total=total, facets=facets or {'port':[dict(value=7547,count=10)]})).encode())


class ClientTests(unittest.TestCase):
    def test_numeric_ports_and_credential_redaction(self):
        urls = []
        def opener(url, **kwargs):
            urls.append(url)
            return response()
        client = m.CountClient('test-secret', opener=opener)
        data = client.count('port:7547', 'port:10')
        self.assertEqual(data['facets']['port'][0]['value'], 7547)
        self.assertTrue(urls[0].startswith('https://api.shodan.io/shodan/host/count?'))
        self.assertNotIn('/search', urls[0])

    def test_429_retried_with_retry_after(self):
        waits, calls = [], []
        def opener(url, **kwargs):
            calls.append(url)
            if len(calls)==1:
                raise urllib.error.HTTPError(url,429,'test-secret',{'Retry-After':'7'},None)
            return response()
        client=m.CountClient('test-secret',opener=opener,sleep=waits.append,clock=lambda:0)
        self.assertEqual(client.count('q','org:100')['total'],10)
        self.assertIn(7,waits)
        self.assertEqual(client.requests,2)

    def test_auth_failure_stops_without_leaking_key(self):
        def opener(url, **kwargs):
            raise urllib.error.HTTPError(url,403,'test-secret',{},None)
        client=m.CountClient('test-secret',opener=opener,sleep=lambda _:None)
        with self.assertRaises(m.CountError) as caught:
            client.count('q','org:100')
        self.assertTrue(caught.exception.fatal)
        self.assertNotIn('test-secret',str(caught.exception))
        self.assertEqual(client.requests,1)

    def test_request_budget_counts_retries(self):
        def opener(url, **kwargs):
            raise urllib.error.URLError('test-secret')
        client=m.CountClient('test-secret',max_requests=1,opener=opener,sleep=lambda _:None)
        with self.assertRaises(m.RequestBudget):
            client.count('q','org:100')
        self.assertEqual(client.requests,1)

    def test_rate_limit_between_successful_requests(self):
        clock=[0.0];starts=[]
        def sleep(seconds):clock[0]+=seconds
        def opener(url,**kwargs):starts.append(clock[0]);return response()
        client=m.CountClient('test',opener=opener,sleep=sleep,clock=lambda:clock[0],interval=1.1)
        client.count('a','port:10');client.count('b','port:10')
        self.assertGreaterEqual(starts[1]-starts[0],1.1)

    def test_bad_response_is_not_zero(self):
        client=m.CountClient('test',opener=lambda *a,**k:io.BytesIO(b'{"error":"test-secret"}'),sleep=lambda _:None)
        with self.assertRaises(m.CountError) as caught:client.count('q','org:100')
        self.assertNotIn('test-secret',str(caught.exception))

    def test_cli_configuration_precedence(self):
        with tempfile.TemporaryDirectory() as directory:
            home=Path(directory)
            self.assertEqual(m.cli_config_dir(home),home/'.config/shodan')
            (home/'.shodan').mkdir()
            self.assertEqual(m.cli_config_dir(home),home/'.shodan')
            (home/'.shodan/api_key').write_text('cli-test-key\n')
            with patch.dict(os.environ, {'SHODAN_API_KEY':''}):
                self.assertEqual(m.load_key(home/'.shodan'),'cli-test-key')


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.out=Path(self.temp.name)/'snapshot-20261008-2227';self.out.mkdir()
        self.jobs=[('line','Line','"Line"',m.BASE_FACETS),('denominator-park','denominator-park','port:7547','country:250')]
        for slug,name,q,facets in self.jobs:
            m.save(self.out/f'{slug}.json',dict(name=name,dork=q,total=25,collection_status='ok',taken='20261008-2227',countries=[dict(value='US',count=20),dict(value='GB',count=5)],asn=[],ports=[]))
        m.save(self.out/'manifest.json',dict(taken='20261008-2227',lines=[],errors=0))
        self.calls=[]
        calls=self.calls
        class FakeClient:
            def __init__(self,key,interval,max_requests):self.requests=0;self.maximum=max_requests
            def count(self,query,facets):
                if self.maximum and self.requests>=self.maximum:raise m.RequestBudget()
                self.requests+=1;calls.append(query)
                return dict(total=10,facets=dict(org=[dict(value='Operator',count=7)],asn=[dict(value='AS1',count=10)]))
        self.client=FakeClient
        self.job_patch=patch.object(m,'base_jobs',return_value=self.jobs);self.job_patch.start()
        self.catalog_patch=patch.object(m,'catalog_jobs',return_value=[]);self.catalog_patch.start()
        self.facts_patch=patch.object(m,'fact_plan',return_value={});self.facts_patch.start()
        self.env_patch=patch.dict(os.environ,{'SHODAN_API_KEY':'fake-key'});self.env_patch.start()

    def tearDown(self):
        self.env_patch.stop();self.job_patch.stop();self.catalog_patch.stop();self.facts_patch.stop();self.temp.cleanup()

    def run_collect(self,*flags):
        args=m.parser().parse_args(list(flags))
        with contextlib.redirect_stdout(io.StringIO()):return m.collect(args,self.client)

    def test_dry_run_never_reads_key_or_writes(self):
        before=(self.out/'manifest.json').read_bytes()
        with patch.object(m,'load_key',side_effect=AssertionError('key read')):
            self.assertEqual(self.run_collect('--drill-only',str(self.out),'--dry-run'),0)
        self.assertFalse(self.calls)
        self.assertEqual(before,(self.out/'manifest.json').read_bytes())

    def test_fresh_collection_syncs_facts_only_after_successful_resume(self):
        root = self.out.parent
        facts_path = root/'data/mapdata/facts.json'
        m.save(facts_path, {'line': [dict(label='Current prose', dork='"Line"', count=25)]})
        before = facts_path.read_bytes()
        target = root/'fresh'
        with patch.object(m, 'ROOT', root):
            self.assertEqual(self.run_collect('--output-dir',str(target),'--skip-stickers','--max-requests','1'),3)
            self.assertEqual(facts_path.read_bytes(), before)
            self.assertEqual(self.run_collect('--resume',str(target)),0)
        fact = m.read(facts_path)['line'][0]
        self.assertEqual(fact['count'],10)
        self.assertEqual(fact['historical_count'],25)
        self.assertEqual(fact['collection_source']['snapshot'],target.name)
        self.assertEqual(fact['collection_source']['run_id'],m.read(target/'manifest.json')['plan']['id'])

    def test_scoped_collection_does_not_sync_source_facts(self):
        target = self.out.parent/'new'
        with patch.object(m, 'sync_facts', side_effect=AssertionError('scoped run must not sync')):
            self.assertEqual(self.run_collect('--from-snapshot',str(self.out),'--output-dir',str(target),
                                             '--only','line','--skip-stickers'),0)

    def test_resume_continues_only_missing_pairs_and_preserves_base(self):
        base=(self.out/'line.json').read_bytes()
        self.assertEqual(self.run_collect('--drill-only',str(self.out),'--max-requests','1'),3)
        self.assertEqual(m.read(self.out/'manifest.json')['status'],'paused')
        self.assertEqual(self.run_collect('--resume',str(self.out)),0)
        manifest=m.read(self.out/'manifest.json')
        self.assertEqual(manifest['status'],'complete')
        self.assertEqual(manifest['org_drill']['completed'],2)
        self.assertEqual(manifest['org_drill']['pending'],0)
        self.assertEqual(len(self.calls),2)
        self.assertEqual(base,(self.out/'line.json').read_bytes())
        cell=m.read(self.out/'org-drill/line--US.json')
        self.assertEqual(cell['facet_meta']['org']['remainder'],3)
        self.assertEqual(cell['requested_facets'],'org:100,asn:100')

    def test_operator_resume_cannot_skip_pending_pairs(self):
        self.assertEqual(self.run_collect('--drill-only',str(self.out),'--max-requests','1'),3)
        before=(self.out/'manifest.json').read_bytes()
        with self.assertRaisesRegex(ValueError,'conflicts'):
            self.run_collect('--resume',str(self.out),'--skip-drill')
        self.assertEqual(before,(self.out/'manifest.json').read_bytes())

    def test_copy_preserves_source_and_resume_freezes_limits(self):
        before={str(p.relative_to(self.out)):p.read_bytes() for p in self.out.rglob('*') if p.is_file()}
        target=self.out.parent/'new'
        self.assertEqual(self.run_collect('--from-snapshot',str(self.out),'--output-dir',str(target),
                         '--drill-countries','1','--org-limit','25','--skip-stickers','--max-requests','1'),0)
        self.assertEqual(self.run_collect('--resume',str(target)),0)
        plan=m.read(target/'manifest.json')['plan']
        self.assertEqual(plan['options']['org_limit'],25)
        self.assertEqual(plan['options']['drill_countries'],1)
        self.assertEqual(len(self.calls),1)
        self.assertEqual(before,{str(p.relative_to(self.out)):p.read_bytes() for p in self.out.rglob('*') if p.is_file()})
        with self.assertRaisesRegex(ValueError,'conflicts'):
            self.run_collect('--resume',str(target),'--org-limit','100')

    def test_completed_resume_preserves_history_bytes(self):
        target=self.out.parent/'new'
        self.assertEqual(self.run_collect('--from-snapshot',str(self.out),'--output-dir',str(target),'--skip-stickers'),0)
        before={str(p.relative_to(target)):p.read_bytes() for p in target.rglob('*') if p.is_file()}
        calls=len(self.calls)
        self.assertEqual(self.run_collect('--resume',str(target)),0)
        self.assertEqual(len(self.calls),calls)
        self.assertEqual(before,{str(p.relative_to(target)):p.read_bytes() for p in target.rglob('*') if p.is_file()})

    def test_completed_dry_resume_does_not_build_or_write(self):
        target=self.out.parent/'new'
        self.assertEqual(self.run_collect('--from-snapshot',str(self.out),'--output-dir',str(target),'--skip-stickers'),0)
        before=(target/'manifest.json').read_bytes()
        with patch.object(m.subprocess,'run',side_effect=AssertionError('dry run must not build')):
            self.assertEqual(self.run_collect('--resume',str(target),'--dry-run','--build'),0)
        self.assertEqual((target/'manifest.json').read_bytes(),before)

    def test_dry_copy_does_not_create_output(self):
        target=self.out.parent/'new'
        self.assertEqual(self.run_collect('--from-snapshot',str(self.out),'--output-dir',str(target),'--dry-run'),0)
        self.assertFalse(target.exists())

    def test_only_refreshes_selected_base(self):
        target=self.out.parent/'new'
        unchanged=(self.out/'denominator-park.json').read_bytes()
        self.assertEqual(self.run_collect('--from-snapshot',str(self.out),'--output-dir',str(target),'--only','line',
                                         '--skip-drill','--skip-stickers'),0)
        self.assertEqual(self.calls,['"Line"'])
        self.assertEqual((target/'denominator-park.json').read_bytes(),unchanged)
        self.assertEqual(m.read(target/'line.json')['total'],10)
        self.assertEqual(m.read(self.out/'line.json')['total'],25)

    def test_resume_uses_embedded_queries_after_catalog_changes(self):
        target=self.out.parent/'new'
        queries=[dict(id=f'variant-{i}',parent='line',group='test',query=f'query {i}',facets='org:10',
                      label=dict(en='test',ru='test',es='test',zh='test'),source=dict(file='TODO.md')) for i in range(2)]
        self.catalog_patch.stop()
        with patch.object(m,'catalog_jobs',return_value=queries):
            self.assertEqual(self.run_collect('--queries-only','--output-dir',str(target),'--max-requests','1'),3)
        with patch.object(m,'catalog_jobs',side_effect=AssertionError('must not reload catalog')):
            self.assertEqual(self.run_collect('--resume',str(target)),0)
        self.catalog_patch.start()
        self.assertEqual(self.calls,['query 0','query 1'])
        self.assertEqual(m.read(target/'manifest.json')['variants']['pending'],0)

    def test_invalid_only_fails_before_writes(self):
        target=self.out.parent/'new'
        with self.assertRaisesRegex(ValueError,'Unknown line'):
            self.run_collect('--from-snapshot',str(self.out),'--output-dir',str(target),'--only','typo')
        self.assertFalse(target.exists())

    def test_standalone_queries_do_not_become_latest_atlas_snapshot(self):
        args=m.parser().parse_args(['--queries-only','--dry-run'])
        out,source,plan,_=m.prepare(args)
        self.assertTrue(out.is_relative_to(m.ROOT/'data/research'))
        self.assertIsNone(source)
        self.assertFalse(plan['base_jobs'])

    def test_denominator_is_included_outside_selected_group(self):
        m.catalog_jobs.return_value=[
            dict(id='version',parent='line',group='versions',denominator='total'),
            dict(id='total',parent='line',group='baseline')]
        args=m.parser().parse_args(['--queries-only','--query-group','versions'])
        _,_,plan,_=m.prepare(args)
        self.assertEqual({q['id'] for q in plan['queries']},{'version','total'})

    def test_default_includes_previous_exclusions(self):
        rec=m.read(self.out/'line.json')
        jobs=m.drill_jobs({'huaweihomegateway':rec,'genieacs-admin-ui':rec,'denominator-park':rec})
        self.assertEqual(len(jobs),4)
        self.assertEqual(len(m.drill_jobs({'a':rec,'b':rec},1,1)),1)

    def test_country_filter_not_confused_with_quoted_text(self):
        self.assertEqual(m.country_query('"country:US"','US'),'"country:US" country:US')
        self.assertEqual(m.country_query('"Line" country:US','US'),'"Line" country:US')

    def test_real_snapshot_plan_covers_all_pairs(self):
        snapshot=ROOT/'data/mapdata/snapshot-20261008-2227'
        records={f.stem:m.read(f) for f in snapshot.glob('*.json') if f.name not in ('manifest.json','stickers.json')}
        jobs=m.drill_jobs(records)
        self.assertEqual(len(jobs),2363)
        self.assertEqual(len({j[0] for j in jobs}),2363)


class FactCatalogTests(unittest.TestCase):
    def test_every_fact_query_has_an_exact_collection_job(self):
        jobs=[dict(id=s,query=q) for s,_,q,_ in m.base_jobs()]
        facts=m.fact_plan(jobs,m.catalog_jobs())
        self.assertTrue(facts)
        self.assertTrue(all(f.get('collection_ref') for items in facts.values() for f in items))

    def test_missing_fact_query_fails_instead_of_silently_skipping_it(self):
        with self.assertRaisesRegex(ValueError,'Uncollected facts queries'):
            m.bind_facts({'line':[dict(dork='"line" port:1234')]},[dict(id='line',query='"line"')],[])

    def test_distinct_query_is_not_substituted_by_a_narrower_query(self):
        with self.assertRaisesRegex(ValueError,'Uncollected facts queries'):
            m.bind_facts({'line':[dict(dork='"line"')]},[],[dict(id='narrow',query='"line" "Digest"')])

    def test_duplicate_observations_share_one_query_without_mutating_source(self):
        facts={'line':[dict(dork='"line"',count=1),dict(dork='"line"',count=2)]}
        bound=m.bind_facts(facts,[dict(id='line',query='"line"')],[])
        self.assertEqual(bound['line'][0]['collection_ref'],bound['line'][1]['collection_ref'])
        self.assertNotIn('collection_ref',facts['line'][0])


if __name__=='__main__':unittest.main()
