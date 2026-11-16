import json,sys
d=json.load(open(sys.argv[1]))['data']['productVariants']
out=json.load(open('soldout.json')) if len(sys.argv)>2 else []
out+=[{'v':n['id'],'q':n['inventoryQuantity'],'pol':n['inventoryPolicy'],'p':n['product']['id'],'t':n['product']['title'],'type':n['product']['productType'],'tot':n['product']['totalInventory']} for n in d['nodes']]
json.dump(out,open('soldout.json','w')); print(len(out),len({x['p'] for x in out}),d['pageInfo'])
