import json,sys
d=json.load(open(sys.argv[1]))['data']['nodes']
try: out=json.load(open('sizes/prods.json'))
except: out=[]
for n in d:
  n.pop('descriptionHtml',None); out.append(n)
json.dump(out,open('sizes/prods.json','w'),ensure_ascii=False)
print(len(out),[n['variants']['pageInfo']['hasNextPage'] for n in d].count(True))
