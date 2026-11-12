"""Evidence boundaries, query scope, and historical isolation of management data."""
import copy
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from management import infrastructure_jobs, read_evidence, read_measurements, profile_measurements

class ManagementTests(unittest.TestCase):
    def setUp(self):
        with (ROOT/'registry.csv').open() as f:self.registry={r['id']:r for r in csv.DictReader(f)}
        self.evidence=read_evidence(ROOT,self.registry)

    def test_catalog_uses_certificate_scope_and_safe_aggregate_facets(self):
        jobs=infrastructure_jobs(ROOT)
        self.assertEqual(len(jobs),8)
        self.assertTrue(all(q['query'].startswith('ssl.cert.') for q in jobs))
        self.assertTrue(all('ssl.cert.fingerprint:100' in q['facets'] for q in jobs))
        self.assertTrue(all('parent' not in q for q in jobs))

    def test_old_snapshot_does_not_gain_current_measurements(self):
        old=ROOT/'data/mapdata/snapshot-20261111-172255'
        self.assertEqual(read_measurements(old,json.loads((old/'manifest.json').read_text())),{})
        observations=profile_measurements(self.evidence,{})
        self.assertTrue(all(p['total'] is None and p['status']=='not-collected' for p in observations.values()))

    def test_profiles_share_measurements_but_never_claim_operator_match(self):
        variants={'huaweihomegateway':[dict(id='huawei-port-8085-co',total=12,taken='2026-11-12T15:00:00+00:00',orgs=[dict(value='Label',count=7)],facet_meta={'org':{'remainder':5}})]}
        obs=profile_measurements(self.evidence,variants)
        self.assertEqual(obs['huawei-profile-edatel'],obs['huawei-profile-une'])
        self.assertEqual(obs['huawei-profile-edatel']['status'],'observed')
        self.assertEqual(obs['huawei-profile-edatel']['remainder'],5)
        self.assertTrue(all(p['operator_status']=='unverified' for p in self.evidence['profiles']))

    def test_reject_private_fields_in_public_measurement(self):
        source=ROOT/'data/mapdata/snapshot-20261112-150712/infrastructure/tls-cwmp-cn.json'
        record=json.loads(source.read_text())
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);(folder/'infrastructure').mkdir()
            target=folder/'infrastructure/tls-cwmp-cn.json'
            for key in ('ip_str','acs_url','credentials','raw_banner'):
                bad={**record,key:'must not publish'};target.write_text(json.dumps(bad))
                with self.assertRaises(ValueError):read_measurements(folder,{})
            target.write_text(json.dumps(record))
            plan=dict(id=record['run_id'],infrastructure_queries=[dict(id=record['id'],query=record['dork']+' country:GB',facets=record['requested_facets'])])
            with self.assertRaisesRegex(ValueError,'outdated'):read_measurements(folder,dict(plan=plan))

    def test_wrong_line_port_or_country_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'data').mkdir()
            (root/'MANAGEMENT-INFRASTRUCTURE.md').write_text('Public source')
            catalog=json.loads((ROOT/'data/collection-queries.json').read_text())
            (root/'data/collection-queries.json').write_text(json.dumps(catalog))
            for mutation in [dict(port=7547),dict(country='DK'),dict(query_id='huawei-port-51005')]:
                bad=copy.deepcopy(self.evidence);bad['profiles'][0].update(mutation)
                (root/'data/management-evidence.json').write_text(json.dumps(bad))
                with self.assertRaisesRegex(ValueError,'bind line'):read_evidence(root,self.registry)

if __name__=='__main__':unittest.main()
