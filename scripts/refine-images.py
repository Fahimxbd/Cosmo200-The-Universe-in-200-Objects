import json, pathlib, urllib.request, urllib.parse, concurrent.futures, re
p=pathlib.Path(__file__).resolve().parents[1]/'public/data/objects.json';d=json.loads(p.read_text());all=[o for l in d['levels'] for o in l['objects']]
queries={1:('Hubble Ultra Deep Field',['ultra deep field','extreme deep']),3:('Virgo Supercluster',['virgo supercluster']),7:('Milky Way panorama',['milky way']),8:('Andromeda galaxy',['andromeda','m31']),13:('M64',['m64','black eye']),22:("Hoag",["hoag"]),23:('M81',['m81','bode']),24:('Centaurus B',['centaurus b','pks 1343']),41:('NGC 6543',['6543',"cat's eye"]),42:('NGC 6302',['6302']),45:('NGC 7635',['7635','bubble nebula']),48:('IC 1805',['1805','heart nebula']),51:('IC 1396',['1396',"elephant"]),54:('M13 globular',['m13','messier 13']),59:('Sirius star',['sirius']),61:('Proxima Centauri',['proxima centauri']),70:('Kepler-47',['kepler-47']),71:('TOI-700',['toi-700','toi 700']),72:('TOI-1452',['toi-1452']),73:('LHS 1140',['lhs 1140']),74:('LHS 3844',['lhs 3844']),75:('L 98-59',['l 98-59']),76:('GJ 1214',['gj 1214','gj1214']),77:('Gliese 581',['gliese 581']),78:('Gliese 876',['gliese 876']),79:('Gliese 667',['gliese 667']),80:('Gliese 832',['gliese 832']),82:('51 Pegasi',['51 pegasi']),83:('HD 209458',['209458']),89:('Beta Pictoris',['beta pictoris']),97:('Ross 128',['ross 128']),99:('K2-18',['k2-18']),100:('WASP-12',['wasp-12']),101:('WASP-39',['wasp-39']),102:('WASP-76',['wasp-76']),103:('WASP-121',['wasp-121']),104:('PSR B1257',['1257']),106:('Capella star',['capella']),109:('Venus planet',['venus']),110:('Earth blue marble',['blue marble']),111:('Moon lunar',['moon','lunar']),112:('Mars planet',['mars']),113:('Jupiter planet',['jupiter']),115:('Saturn planet',['saturn']),117:('Uranus planet',['uranus']),118:('Neptune planet',['neptune']),119:('Pluto New Horizons',['pluto']),122:('Haumea',['haumea']),123:('Makemake',['makemake']),144:('Proteus Neptune',['proteus']),149:('Styx Pluto',['styx']),164:('Leda Jupiter',['leda']),189:('Puck Uranus',['puck']),191:('Juliet Uranus',['juliet']),194:('Rosalind Uranus',['rosalind']),197:('Ophelia Uranus',['ophelia'])}
# Correct queries using names, rather than relying on numbering when series differ.
for o in all:
 if o['id'] in queries and o['level']==4:
  queries[o['id']]=(o['name'],[o['name'].lower()])
def norm(t):return re.sub(r'[^a-z0-9]+',' ',t.lower()).strip()
def resolve(o):
 q,terms=queries[o['id']];old=o['image'];o['image']=None
 try:
  u='https://images-api.nasa.gov/search?'+urllib.parse.urlencode({'q':q,'media_type':'image','page_size':60})
  with urllib.request.urlopen(u,timeout=25) as r:items=json.load(r)['collection']['items']
  scored=[]
  for it in items:
   m=it.get('data',[{}])[0];title=m.get('title','');desc=re.sub('<[^>]*>','',m.get('description',''));t=norm(title);body=norm(desc);links=[x['href'] for x in it.get('links',[]) if x.get('render')=='image']
   if not links:continue
   if not any(norm(term) in body or norm(term) in t for term in terms):continue
   if any(w in t for w in ['rollout','mission patch','logo','press conference','celebration','microphone','flight center','ksc','icescape','capsule','front view in flight','crew portrait']):continue
   if o.get('parent') and o['type']=='Moon' and norm(o['parent']) not in body+' '+t:continue
   if o['name'] in ['Capella','Sirius'] and 'star' not in body:continue
   score=sum(25 if norm(term) in t else 1 for term in terms)
   if any(w in t for w in ['panorama','portrait','blue marble','full disk','global view']):score+=8
   if any(w in t for w in ['candidate','animation','gif','diagram','montage','comparison']):score-=5
   scored.append((score,m,links[0],title,desc))
  if scored:
   _,m,url,title,desc=max(scored,key=lambda x:x[0]);art=any(w in (title+' '+desc[:1000]).lower() for w in ['artist','illustration','concept','simulation','visualization','diagram','depiction'])
   o['image']={'url':url.replace('http:','https:'),'title':title,'credit':m.get('photographer') or 'NASA / '+m.get('center','Image and Video Library'),'nasaId':m['nasa_id'],'kind':'Illustration / visualization' if art else 'NASA archive image','sourceUrl':'https://images.nasa.gov/details/'+urllib.parse.quote(m['nasa_id'],safe=''),'note':'See the original NASA caption for processing and full credit.'}
 except Exception:pass
 return o['id'],o['name'],o['image']['title'] if o['image'] else 'NO MATCH'
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 for r in pool.map(resolve,[o for o in all if o['id'] in queries]):print(*r,sep=' | ')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
