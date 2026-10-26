import json,csv
H={tuple(k.split('|',1)):v for k,v in json.load(open('photo/hashes.json')).items()}
P={(r['store'],r['product']):r for r in csv.DictReader(open('data_all/products.csv'))}
NP=[r for r in csv.DictReader(open('data_niaali/products.csv'))]
items=json.load(open('page3/items.json'))
loc={}
for i,it in enumerate(items):
    for s in it['stores']: loc[(s['store'],s['product'])]=i
dist=lambda a,b:min(bin(x^y).count('1') for x in H[a] for y in H[b])
def row(r):return dict(store='Niaali',product=r['product'],orders=int(r['orders']),refunds=int(r['refund_orders']),quality=int(r['quality_refund_orders']),nad=int(r['not_as_described_cases']),rate=float(r['problem_rate']),priority=r['priority'])
added=0;new=0;skipped=[]
for r in NP:
    k=('Niaali',r['product'])
    if k not in H: continue
    m=[b for b in H if b[0]!='Niaali' and dist(k,b)<=2]
    groups={loc.get(b,('single',b)) for b in m}
    if not m: continue
    if len(groups)!=1: skipped.append((r['product'],len(groups)));continue
    g=next(iter(groups))
    if isinstance(g,int):
        it=items[g]
        if any(s['store']=='Niaali' for s in it['stores']):skipped.append((r['product'],'dup'));continue
        it['stores'].append(row(r));it['evidence']+='; identical photo at Niaali';added+=1
    else:
        b=g[1];o=P[b]
        items.append(dict(id=f'm{len([x for x in items if x["kind"]=="both"])+1+new+100:03d}',kind='both',title=b[1],stores=[dict(store=b[0],product=b[1],orders=int(o['orders']),refunds=int(o['refund_orders']),quality=int(o['quality_refund_orders']),nad=int(o['not_as_described_cases']),rate=float(o['problem_rate']),priority=o['priority']),row(r)],priority='High' if 'High' in (o['priority'],r['priority']) else ('Medium' if 'Medium' in (o['priority'],r['priority']) else ''),confidence='High',evidence='Identical photo in both stores'));new+=1;loc[b]=len(items)-1
used={(s['store'],s['product']) for it in items for s in it['stores']}
items=[it for it in items if not (it['kind']!='both' and (it['stores'][0]['store'],it['stores'][0]['product']) in used and it['stores'][0]['store']!='Niaali' and False)]
# remove single-store items now merged
res=[]
for it in items:
    if it['kind']!='both' and len(it['stores'])==1 and loc.get((it['stores'][0]['store'],it['stores'][0]['product']),-1)!=-1 and items[loc[(it['stores'][0]['store'],it['stores'][0]['product'])]] is not it: continue
    res.append(it)
items=res
n=0
for r in NP:
    if ('Niaali',r['product']) not in {(s['store'],s['product']) for it in items for s in it['stores']}:
        n+=1;items.append(dict(id=f'n{n:03d}',kind='Niaali',title=r['product'],stores=[row(r)],priority=r['priority'],confidence='',evidence=''))
order={'High':0,'Medium':1,'':2}
b=[i for i in items if i['kind']=='both'];o=[i for i in items if i['kind']!='both']
b.sort(key=lambda i:(order[i['priority']],-sum(s['orders'] for s in i['stores'])))
items=b+o
json.dump(items,open('page3/items.json','w'),ensure_ascii=False)
print('Niaali added to existing',added,'new groups',new,'skipped',skipped,'| items',len(items),'matched',len(b),'niaali-only',n)
