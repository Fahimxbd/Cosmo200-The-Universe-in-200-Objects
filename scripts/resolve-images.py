"""Resolve public NASA Image Library metadata at authoring time; no runtime API/key."""
import json, pathlib, urllib.request, urllib.parse, concurrent.futures, re
p=pathlib.Path(__file__).resolve().parents[1]/'public/data/objects.json'
d=json.loads(p.read_text()); objects=[o for l in d['levels'] for o in l['objects']]
def resolve(o):
    q=o['nasaQuery']; q={'Observable Universe':'Hubble Ultra Deep Field','Milky Way':'Milky Way galaxy','Moon':'Earth Moon','Sun':'Sun SDO','Solar System':'Solar System planets'}.get(q,q)
    u='https://images-api.nasa.gov/search?'+urllib.parse.urlencode({'q':q,'media_type':'image','page_size':12})
    try:
        with urllib.request.urlopen(u,timeout=25) as r: items=json.load(r)['collection']['items']
        candidates=[]
        for item in items:
            m=item.get('data',[{}])[0]; title=m.get('title',''); description=re.sub('<[^>]*>','',m.get('description',''))
            links=[x['href'] for x in item.get('links',[]) if x.get('render')=='image']
            if not links: continue
            words=[w.lower() for w in re.findall(r'[\w-]+',q) if w.lower() not in ['the','galaxy','nebula','cluster','supercluster']]
            score=sum(4 if w in title.lower() else 1 if w in description.lower() else -5 for w in words)
            if any(w in title.lower() for w in ['logo','patch','astronaut','press conference','briefing']): score-=20
            candidates.append((score,m,links[0],title,description))
        if candidates:
            score,m,url,title,desc=max(candidates,key=lambda x:x[0])
            if score>0:
                art=any(w in (title+' '+desc[:600]).lower() for w in ['artist','illustration','concept','simulation','visualization','diagram','depiction'])
                o['image']={'url':url.replace('http:','https:'),'title':title,'credit':m.get('photographer') or 'NASA / '+m.get('center','Image and Video Library'),'nasaId':m['nasa_id'],'kind':'Illustration / visualization' if art else 'NASA archive image','sourceUrl':'https://images.nasa.gov/details/'+urllib.parse.quote(m['nasa_id'],safe=''),'note':'Archive search match; see the original caption for the subject, processing, and full credit.'}
        return bool(o['image'])
    except Exception as e: return False
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results=list(pool.map(resolve,objects))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('NASA image records:',sum(results),'/ 200')
print('Without verified archive match:',', '.join(o['name'] for o in objects if not o['image']))
