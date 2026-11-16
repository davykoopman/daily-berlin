import json,sys
d=json.load(open(sys.argv[1]))['data']['products']
out=json.load(open('prices.json')) if len(sys.argv)>2 else []
for n in d['nodes']:
    out.append({'t':n['title'],'type':n['productType'],'tags':n['tags'],'p':float(n['priceRangeV2']['minVariantPrice']['amount']),'pmax':float(n['priceRangeV2']['maxVariantPrice']['amount']),
      'c':float((n['compareAtPriceRange'] or {}).get('minVariantCompareAtPrice',{}).get('amount') or 0),'cmax':float((n['compareAtPriceRange'] or {}).get('maxVariantCompareAtPrice',{}).get('amount') or 0)})
json.dump(out,open('prices.json','w')); print(len(out), d['pageInfo'])
