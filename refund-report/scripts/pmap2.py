import json,csv
H={tuple(k.split('|',1)):v for k,v in json.load(open('photo/hashes.json')).items()}
P=list(csv.DictReader(open('data_all/products.csv')))
byk={(r['store'],r['product']):r for r in P}
old={(r['daily_berlin_product'],r['davento_product']):r for r in csv.DictReader(open('photo/old_map.csv'))}
newname={'Herren Bikerjacke mit Reißverschluss':'Men biker jacket with zip','Herren Cargojacke im Military-Stil':'Men military cargo jacket','Herren Weste mit vielen Taschen Outdoor':'Men utility vest with pockets'}
db=[k for k in H if k[0]=='Daily Berlin'];dv=[k for k in H if k[0]=='Davento']
cand=[]
for a in db:
    for b in dv:
        d=min(bin(x^y).count('1') for x in H[a] for y in H[b])
        if d<=2:cand.append((d,a[1],b[1]))
# one Davento product shared by several DB products -> not merged
from collections import Counter
cd=Counter(b for _,_,b in cand);ca=Counter(a for _,a,_ in cand)
rows=[];skipped=[]
for d,a,b in sorted(cand):
    if cd[b]>1 or ca[a]>1: skipped.append((a,b));continue
    o=old.get((a,b))
    rows.append(dict(master=o['master'] if o else newname.get(a,a),db=a,dav=b,photo='Identical photo' if d==0 else 'Near-identical photo',old=o))
DC=('Damen Clogs mit verstellbarer Schnalle für den Alltag','Zoccoli da donna con fibbia regolabile per il tempo libero')
rows.append(dict(master=old[DC]['master'],db=DC[0],dav=DC[1],photo='Identical photo',old=old[DC]))
usedp={r['db'] for r in rows}|{r['dav'] for r in rows}
for k,o in old.items():
    if k!=DC and ('Daily Berlin',k[0]) in byk and ('Davento',k[1]) in byk and k[0] not in usedp and k[1] not in usedp and (k not in {(r['db'],r['dav']) for r in rows}):
        rows.append(dict(master=o['master'],db=k[0],dav=k[1],photo='Title and price only, photos not confirmed',old=o,med=True));usedp|={k[0],k[1]}
for r in rows:
    if r['db']=='Herren Bikerjacke mit Reißverschluss': r['med']=True; r['photo']='Identical photo, but Davento also has a similar jacket (Giacca Uomo in Stile Biker); please confirm'
photo_pairs={(r['db'],r['dav']) for r in rows}
unverified=[o for k,o in old.items() if k not in photo_pairs]
print(len(rows),'photo pairs; skipped',skipped);print('old title-only pairs not confirmed by photo:',[(o['daily_berlin_product'][:40],o['davento_product'][:40]) for o in unverified])
items=[];n=0
for r in rows:
    n+=1;sd=[]
    for st,p in(('Daily Berlin',r['db']),('Davento',r['dav'])):
        x=byk[(st,p)];sd.append(dict(store=st,product=p,orders=int(x['orders']),refunds=int(x['refund_orders']),quality=int(x['quality_refund_orders']),nad=int(x['not_as_described_cases']),rate=float(x['problem_rate']),priority=x['priority']))
    pr='High' if any(s['priority']=='High' for s in sd) else ('Medium' if any(s['priority']=='Medium' for s in sd) else '')
    ev=r['photo']+('' if r.get('med') else ' in both stores')+('; '+r['old']['evidence'] if r['old'] else '')
    items.append(dict(id=f'm{n:02d}',kind='both',title=r['master'],stores=sd,priority=pr,confidence='Medium' if r.get('med') else 'High',evidence=ev))
order={'High':0,'Medium':1,'':2}
items.sort(key=lambda i:(order[i['priority']],-sum(s['orders'] for s in i['stores'])))
used={(s['store'],s['product']) for i in items for s in i['stores']}
for st,pre in(('Daily Berlin','d'),('Davento','v')):
    k=0
    for r in P:
        if r['store']!=st or (st,r['product']) in used:continue
        k+=1;items.append(dict(id=f'{pre}{k:03d}',kind=st,title=r['product'],stores=[dict(store=st,product=r['product'],orders=int(r['orders']),refunds=int(r['refund_orders']),quality=int(r['quality_refund_orders']),nad=int(r['not_as_described_cases']),rate=float(r['problem_rate']),priority=r['priority'])],priority=r['priority'],confidence='',evidence=''))
json.dump(items,open('page3/items.json','w'),ensure_ascii=False)
mp=[dict(master=i['title'],daily_berlin_product=i['stores'][0]['product'],db_orders=i['stores'][0]['orders'],davento_product=i['stores'][1]['product'],dav_orders=i['stores'][1]['orders'],confidence=i['confidence'],evidence=i['evidence']) for i in items if i['kind']=='both']
w=csv.DictWriter(open('data_all/product_map.csv','w',newline=''),fieldnames=list(mp[0]));w.writeheader();w.writerows(mp)
print(len(items),'items;',sum(i['kind']=='both' for i in items),'matched')
