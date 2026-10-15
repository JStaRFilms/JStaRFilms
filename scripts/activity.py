#!/usr/bin/env python3
"""Public-only, explicitly attributed commit activity. Python 3.10+, stdlib only."""
import argparse, datetime as dt, json, os, pathlib, urllib.request, urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
REPOS=[('Takomi suite','J-StaR-Films-Studios/VibeCode-Protocol-Suite'),('Takomi Code','JStaRFilms/Takomi-Code'),('Melo','JStaRFilms/Melo_School_Management_System'),('JStar Study','JStaRFilms/adaptive-study-game'),('Koe','JStaRFilms/Koe'),('CreativeOS','J-StaR-Films-Studios/CreativeOS'),('Cube Trainer','JStaRFilms/rubiks-cube-trainer'),('NamiStack','JStaRFilms/namistack')]
LOGIN='JStaRFilms'
def get(path):
 headers={'Accept':'application/vnd.github+json','User-Agent':'JStaRFilms-profile-activity'}
 if os.getenv('GH_TOKEN'): headers['Authorization']='Bearer '+os.environ['GH_TOKEN']
 with urllib.request.urlopen(urllib.request.Request('https://api.github.com/'+path,headers=headers),timeout=60) as r: return json.load(r)
def collect(end):
 start=end-dt.timedelta(days=182); rows=[]; commits={}
 for label,repo in REPOS:
  meta=get('repos/'+repo)
  if meta.get('private') is not False: raise RuntimeError('Refusing non-public repository')
  branch=meta['default_branch']; head=get('repos/'+repo+'/commits/'+urllib.parse.quote(branch,safe=''))['sha']
  row={'label':label,'repository':repo,'branch':branch,'head':head,'company':repo.startswith('J-StaR-Films-Studios/'),'commits':[]}
  page=1
  while True:
   query=urllib.parse.urlencode({'sha':head,'author':LOGIN,'since':start.isoformat()+'T00:00:00Z','until':(end-dt.timedelta(days=1)).isoformat()+'T23:59:59Z','per_page':100,'page':page})
   batch=get('repos/'+repo+'/commits?'+query)
   for c in batch:
    # Never infer identity from an email, display name, ownership or committer.
    if (c.get('author') or {}).get('login','').casefold()!=LOGIN.casefold() or len(c['parents'])>1: continue
    day=dt.datetime.fromisoformat(c['commit']['committer']['date'].replace('Z','+00:00')).astimezone(dt.timezone.utc).date()
    if not start<=day<end: continue
    row['commits'].append(c['sha'])
    entry=commits.setdefault(c['sha'],{'sha':c['sha'],'date':str(day),'repositories':[]})
    entry['repositories'].append(repo)
   if len(batch)<100: break
   page+=1
  row['commits']=sorted(set(row['commits']));rows.append(row)
  print(label,len(row['commits']),flush=True)
 return {'schema':1,'login':LOGIN,'start':str(start),'end_exclusive':str(end),'generated_at':dt.datetime.now(dt.timezone.utc).isoformat(),'repositories':rows,'commits':sorted(commits.values(),key=lambda c:(c['date'],c['sha']))}
def main():
 p=argparse.ArgumentParser();p.add_argument('--end',help='Exclusive UTC date, defaults to today');p.add_argument('--offline',action='store_true');a=p.parse_args()
 target=ROOT/'data/activity.json'
 if a.offline: data=json.loads(target.read_text())
 else:
  data=collect(dt.date.fromisoformat(a.end) if a.end else dt.datetime.now(dt.timezone.utc).date())
  # All API calls must succeed before any shipped snapshot is changed.
  target.parent.mkdir(exist_ok=True);temp=target.with_suffix('.tmp');temp.write_text(json.dumps(data,indent=2)+'\n');temp.replace(target)
 from render_assets import render_activity
 render_activity(data)
if __name__=='__main__': main()
