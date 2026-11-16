import json,sys,collections
d=json.load(open(sys.argv[1]))['data']['products']
out=json.load(open('verify.json')) if len(sys.argv)>2 else []
out+=[{'id':n['id'],'type':n['productType'],'g':(n['g'] or {}).get('value'),'a':(n['a'] or {}).get('value')} for n in d['nodes']]
json.dump(out,open('verify.json','w'))
print(len(out),d['pageInfo'],collections.Counter((x['g'],x['a']) for x in out))
