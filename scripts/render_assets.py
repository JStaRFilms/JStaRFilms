"""Deterministic SVGs: no external fonts, scripts, images or network dependencies."""
from pathlib import Path
from html import escape
import datetime as dt,collections
ROOT=Path(__file__).resolve().parents[1]
PALETTES={'light':('#f5f3ed','#202621','#61695e','#d5dacd','#e5e9df'),'dark':('#19221e','#f5f3ed','#b3beb0','#445348','#2a382e')}
def text(x,y,s,size=16,color='#202621',weight=400,extra=''):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(s))}</text>'
def rect(x,y,w,h,c,r=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}"/>'
def svg(w,h,body,title,desc):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'+''.join(body)+'</svg>\n'
def save(name,s):(ROOT/'assets'/name).write_text(s,encoding='utf-8')
def render_activity(data):
 start=dt.date.fromisoformat(data['start']);end=dt.date.fromisoformat(data['end_exclusive']);daily=collections.Counter(c['date'] for c in data['commits']);company={s for r in data['repositories'] if r['company'] for s in r['commits']};total=len(data['commits']);active=len(daily)
 for theme in PALETTES:
  bg,fg,mut,line,empty=PALETTES[theme]
  for mobile in [False,True]:
   w=400 if mobile else 880;h=650 if mobile else 656;pad=24 if mobile else 30
   b=[rect(0,0,w,h,bg),text(pad,33,'THE WORK, OVER TIME',14,fg,700),text(pad,58,f'{start:%d %b} – {end-dt.timedelta(days=1):%d %b %Y} · UTC',13,mut)]
   values=[(f'{total:,}','authored commits'),(str(active),'active days'),(f'{len(company):,}','in studio repos')]
   for i,(v,label) in enumerate(values):
    x=pad+i*(119 if mobile else 279);b +=[text(x,108,v,34,fg,700),text(x,131,label,11 if mobile else 14,mut)]
   # Fixed 26-week strip, each column is seven consecutive days from start.
   size=10 if mobile else 24;gap=3 if mobile else 7;x0=pad;y0=178
   colors=[empty,'#b7cb87','#8daf55','#588230','#36581f'] if theme=='light' else [empty,'#476136','#698841','#a3c25a','#d1f06f']
   for i in range(182):
    day=start+dt.timedelta(days=i);n=daily[str(day)];idx=0 if not n else 1 if n<=3 else 2 if n<=9 else 3 if n<=24 else 4
    x=x0+(i//7)*(size+gap);y=y0+(i%7)*(size+gap)
    b.append(f'<g><title>{day}: {n} commits</title>'+rect(x,y,size,size,colors[idx],2)+'</g>')
   b.append(text(pad,151,'DAILY COMMITS / 26 SEVEN-DAY COLUMNS',10,mut,700))
   last_month=None
   for col in range(26):
    day=start+dt.timedelta(days=col*7)
    if day.month!=last_month:
     b.append(text(x0+col*(size+gap),171,day.strftime('%b'),10,mut));last_month=day.month
   ly=y0+7*(size+gap)+18
   b.append(text(pad,ly,'0',11,mut))
   for i,l in enumerate(['1–3','4–9','10–24','25+']):
    x=pad+25+i*70;b += [rect(x,ly-10,10,10,colors[i+1],2),text(x+15,ly,l,10,mut)]
   top=ly+42;b.append(text(pad,top,'WHERE THOSE COMMITS LANDED',11,mut,700))
   rows=sorted(data['repositories'],key=lambda r:len(r['commits']),reverse=True);maximum=max([len(r['commits']) for r in rows]+[1])
   for i,r in enumerate(rows):
    if mobile: x=pad;y=top+29+i*34;barx=170;barw=153;numx=376
    else:
     col=i//4;ix=i%4;x=pad+col*424;y=top+30+ix*34;barx=x+130;barw=215;numx=x+389
    n=len(r['commits']);b +=[text(x,y,r['label']+(' *' if r['company'] else ''),12,fg),rect(barx,y-10,barw,10,empty,2),rect(barx,y-10,round(barw*n/maximum,2),10,'#e74b32' if r['company'] else '#87a94f',2),text(numx,y,n,12,fg,700,'text-anchor="end"')]
   b +=[text(pad,h-34,'* Studio-owned repository · only JStaRFilms-attributed commits',10,mut),text(pad,h-16,'8 public repositories · non-merge commits · not all GitHub activity',10,mut)]
   save(f'activity-{theme}{"-mobile" if mobile else ""}.svg',svg(w,h,b,'JStaRFilms public authored commit activity',f'{total} unique non-merge commits; {active} active UTC days; {len(company)} commits in selected studio repositories. Full counts and method are in ACTIVITY.md.'))
 lines=['# Activity snapshot','',f'Window: **{start} through {end-dt.timedelta(days=1)}**, complete UTC days.',f'Collected: {data["generated_at"]}.','',f'**{total:,}** unique non-merge commits · **{active}** active days · **{len(company):,}** commits in selected studio repositories.','','| Repository | Authored commits | Default branch |','|---|---:|---|']
 for r in data['repositories']:lines.append(f'| [{r["label"]}](https://github.com/{r["repository"]}) | {len(r["commits"])} | `{r["branch"]}` |')
 lines +=['','## What this counts','','GitHub REST commits API, filtered by `author=JStaRFilms`, then checked again against the returned `author.login`. Only non-merge commits reachable from each repository’s default-branch head are included. Each head is pinned before pagination. The calendar uses the commit’s **committer timestamp in UTC**, not the push date or original author timestamp. A column is seven consecutive days from the printed start date; rows are not fixed Monday–Sunday labels. Color buckets: 0, 1–3, 4–9, 10–24, 25+.','','The total and daily calendar deduplicate commit SHAs across repositories. Repository bars count unique SHAs within each repository, so shared history could make the bars sum to more than the overall total. Studio count is the union of counted SHAs in the two studio-owned repositories. An active day means at least one counted commit. Zero means no qualifying commit in this window, not an abandoned project.','','This is **not** GitHub’s contribution calendar or a productivity score. It excludes private repositories, other public repositories, non-default branches, merges, issues, reviews, PR events and co-authored commits not primarily attributed to this login. Fork history is included only where GitHub identifies JStaRFilms as author; upstream authors are never assigned to John. Squash/rebase history and linked-account attribution affect counts.','','## Source and refresh','','Source: [GitHub REST commits API](https://docs.github.com/en/rest/commits/commits#list-commits). Audit input: [data/activity.json](data/activity.json), containing public SHAs, dates, repo names and captured heads. No emails, commit messages, tokens or private data are exported.','','Run `python scripts/activity.py` to fetch the last 182 complete UTC days and rebuild the SVGs and this table. Run `python scripts/activity.py --offline` to reproduce the visual assets from the saved snapshot. `.github/workflows/activity.yml` supports manual refresh through GitHub Actions. No weekly schedule is enabled. See MAINTENANCE.md for permissions, failures and publishing.']
 (ROOT/'ACTIVITY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
