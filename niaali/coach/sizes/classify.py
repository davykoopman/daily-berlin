import json,collections
P=json.load(open('sizes/prods.json'))
R={'XS':0,'S':1,'M':2,'L':3,'XL':4,'2XL':5,'XXL':5,'3XL':6,'XXXL':6}
def rank(s): return float(s) if s.replace('.','').isdigit() else R[s]
dele=[];mid=[];fullcolor=[]
for p in P:
  groups=collections.defaultdict(list)
  for v in p['variants']['nodes']:
    o={x['name']:x['value'] for x in v['selectedOptions']}
    groups[o.get('Kolor','-')].append((rank(o['Rozmiar']),o['Rozmiar'],v))
  for col,vs in groups.items():
    vs.sort(key=lambda t:t[0])
    out=[ (v['inventoryQuantity']<=0 and v['inventoryPolicy']=='DENY') for _,_,v in vs]
    if not any(out): continue
    if all(out): fullcolor.append((p['title'],col))
    for i,(r,s,v) in enumerate(vs):
      if not out[i]: continue
      below=any(not o for o in out[:i]); above=any(not o for o in out[i+1:])
      rec={'product':p['id'],'title':p['title'],'kolor':col,'rozmiar':s,'variant':v['id'],'sku':v['sku'],'price':v['price'],'compareAt':v['compareAtPrice'],'qty':v['inventoryQuantity']}
      (mid if (below and above) else dele).append(rec)
json.dump({'delete':dele,'middle':mid,'fullcolor':fullcolor},open('sizes/plan.json','w'),ensure_ascii=False,indent=1)
print('delete',len(dele),'middle',len(mid),'total',len(dele)+len(mid))
print('full colours sold out:',fullcolor)
print('--- MIDDLE ---')
for m in mid: print(m['title'][:55],'|',m['kolor'],'|',m['rozmiar'])
# products that would lose all variants?
left=collections.Counter()
for p in P: left[p['id']]=len(p['variants']['nodes'])
for d in dele: left[d['product']]-=1
print('products left with 0 variants:',[k for k,v in left.items() if v<=0])
