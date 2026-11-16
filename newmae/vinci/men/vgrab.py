import json,sys
d=json.load(open(sys.argv[1]))['data']['products']
out=json.load(open('variants.json')) if len(sys.argv)>2 else []
for n in d['nodes']:
    out.append({'id':n['id'],'t':n['title'],'created':n['createdAt'],'type':n['productType'],
      'v':[{'id':v['id'],'p':float(v['price']),'c':float(v['compareAtPrice'] or 0),'cost':float(((v['inventoryItem'] or {}).get('unitCost') or {}).get('amount') or 0)} for v in n['variants']['nodes']]})
json.dump(out,open('variants.json','w')); print(len(out), d['pageInfo'])
