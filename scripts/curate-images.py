"""Apply manually selected NASA media IDs after discovery. Do not auto-publish search matches."""
import json,pathlib,urllib.request,urllib.parse
p=pathlib.Path(__file__).resolve().parents[1]/'public/data/objects.json';d=json.loads(p.read_text());objects={o['id']:o for l in d['levels'] for o in l['objects']}
# These search hits refer to unrelated subjects or cannot establish the depicted object.
for i in [3,22,59,144,164,189,191,194,197]:objects[i]['image']=None
approved={1:'GSFC_20171208_Archive_e001651',48:'PIA13112',111:'PIA12235',115:'PIA01969'}
for i,nasa_id in approved.items():
 u='https://images-api.nasa.gov/search?'+urllib.parse.urlencode({'nasa_id':nasa_id,'media_type':'image'})
 with urllib.request.urlopen(u,timeout=30) as r:items=json.load(r)['collection']['items']
 item=next(x for x in items if x['data'][0]['nasa_id']==nasa_id);m=item['data'][0]
 objects[i]['image']={'url':next(x['href'] for x in item['links'] if x.get('render')=='image'),'title':m['title'],'credit':'NASA / '+m.get('center','Image and Video Library'),'nasaId':nasa_id,'kind':'NASA archive image','sourceUrl':'https://images.nasa.gov/details/'+urllib.parse.quote(nasa_id),'note':'See the original NASA caption for full credit and image processing.'}
objects[7]['radius']=16
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('Curated NASA records',sum(bool(o['image']) for o in objects.values()))
