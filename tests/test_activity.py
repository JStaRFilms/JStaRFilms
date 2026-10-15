"""Checks attribution, exclusions, deduplication, paging, and privacy gate."""
import sys,unittest,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import activity

def commit(sha,login='JStaRFilms',parents=1,date='2026-10-14T10:00:00Z'):
 return {'sha':sha,'author':{'login':login},'parents':[{}]*parents,'commit':{'committer':{'date':date}}}
class ActivityTests(unittest.TestCase):
 def collect(self,batches,private=False):
  def get(path):
   if '/commits?' in path:return batches.pop(0)
   if '/commits/' in path:return {'sha':'pinned-head'}
   return {'private':private,'default_branch':'main'}
  with patch.object(activity,'REPOS',[('Test','example/public')]),patch.object(activity,'get',side_effect=get):
   return activity.collect(dt.date(2026,10,15))
 def test_identity_merge_window(self):
  d=self.collect([[commit('yes'),commit('other','someone'),commit('merge',parents=2),commit('outside',date='2026-10-15T00:00:00Z'),commit('old',date='2026-04-15T23:59:59Z')]])
  self.assertEqual([c['sha'] for c in d['commits']],['yes'])
 def test_private_refused(self):
  with self.assertRaisesRegex(RuntimeError,'non-public'):self.collect([],private=True)
 def test_full_page_continues(self):
  d=self.collect([[commit(str(i)) for i in range(100)],[commit('last')]])
  self.assertEqual(len(d['commits']),101)
 def test_duplicate_sha(self):
  d=self.collect([[commit('same'),commit('same')]])
  self.assertEqual(len(d['commits']),1)
  self.assertEqual(d['repositories'][0]['commits'],['same'])
 def test_saved_snapshot_consistency(self):
  import json
  d=json.loads((activity.ROOT/'data/activity.json').read_text())
  shas={c['sha'] for c in d['commits']}
  self.assertEqual(len(shas),len(d['commits']))
  self.assertEqual(shas,{s for r in d['repositories'] for s in r['commits']})
  self.assertTrue(all(d['start']<=c['date']<d['end_exclusive'] for c in d['commits']))
 def test_offline_graph_is_valid_utf8_xml(self):
  import json,tempfile,xml.etree.ElementTree as ET
  import render_assets
  data=json.loads((activity.ROOT/'data/activity.json').read_text())
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);(root/'assets').mkdir()
   with patch.object(render_assets,'ROOT',root):render_assets.render_activity(data)
   assets=list((root/'assets').glob('activity-*.svg'))
   self.assertEqual(len(assets),4)
   for asset in assets:
    ET.fromstring(asset.read_text(encoding='utf-8'))
   self.assertIn('182 complete UTC days',(root/'ACTIVITY.md').read_text(encoding='utf-8'))
if __name__=='__main__':unittest.main()
