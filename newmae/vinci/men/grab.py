import json,sys
d=json.load(open(sys.argv[1]))['data']
p=d['products']; out=json.load(open('allw.json')) if len(sys.argv)>2 else []
out+=[{'handle':n['handle'],'type':n['productType']} for n in p['nodes']]
json.dump(out,open('allw.json','w'))
print(d.get('productsCount'), len(out), p['pageInfo'])
