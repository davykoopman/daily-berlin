import json,sys,collections
d=json.load(open(sys.argv[1]))['data']['products']
out=json.load(open('prods.json')) if len(sys.argv)>2 else []
out+=[{'id':n['id'],'type':n['productType'],'g':(n['g'] or {}).get('value'),'gt':(n['g'] or {}).get('type'),'a':(n['a'] or {}).get('value'),'at':(n['a'] or {}).get('type')} for n in d['nodes']]
json.dump(out,open('prods.json','w'))
print(len(out),d['pageInfo'],collections.Counter((x['g'],x['a'],x['at']) for x in out))
