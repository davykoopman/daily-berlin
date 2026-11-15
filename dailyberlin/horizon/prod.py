import json,re
def load(f): return json.loads(re.sub(r'^/\*.*?\*/','',open(f).read(),flags=re.S))
H='/home/user/daily-berlin/dailyberlin/horizon-orig/'; I='/home/user/daily-berlin/dailyberlin/impulse-content/'
p=load(H+'templates/product.json'); ip=load(I+'templates/product.json')
det=p['sections']['main']['blocks']['product-details']
def text(t,preset='rte',align='left'): return {"type":"text","settings":{"text":t,"type_preset":preset,"alignment":align,"width":"100%"}}
pts=[('truck','Versandkostenfrei innerhalb Deutschlands'),('return','60 Tage Rückgaberecht'),('chat_bubble','24/7 Kundenservice')]
rows={}
for i,(ic,t) in enumerate(pts):
    rows[f"sp_{i}"]={"type":"group","settings":{"content_direction":"row","vertical_on_mobile":False,"horizontal_alignment":"flex-start","vertical_alignment":"center","gap":10,"width":"fill","width_mobile":"fill"},
      "blocks":{f"sp_{i}_i":{"type":"icon","settings":{"icon":ic,"width":22}},f"sp_{i}_t":text(f"<p>{t}</p>")},"block_order":[f"sp_{i}_i",f"sp_{i}_t"]}
det['blocks']['sales_points']={"type":"group","name":"Vorteile","settings":{"content_direction":"column","horizontal_alignment_flex_direction_column":"flex-start","gap":8,"width":"fill","width_mobile":"fill"},"blocks":rows,"block_order":list(rows)}
det['blocks']['pay_icons']={"type":"payment-icons","settings":{"horizontal_alignment":"flex-start","gap":6}}
kiwi=ip['sections']['main']['blocks']['kiwi_size_chart_recommender_kiwi_sizing_PEYjzP']
det['blocks']['kiwi_size']=kiwi
tab=ip['sections']['main']['blocks']['tab']['settings']
det['blocks']['info_acc']={"type":"accordion","settings":{"icon":"plus","dividers":True,"type_preset":"h6"},
  "blocks":{"acc_ship":{"type":"_accordion-row","settings":{"heading":tab['title']},"blocks":{"acc_ship_t":text(tab['content'])},"block_order":["acc_ship_t"]},
            "acc_ret":{"type":"_accordion-row","settings":{"heading":"Rückgabe"},"blocks":{"acc_ret_t":text("<p>60 Tage Rückgaberecht für ungetragene Artikel im Originalzustand. Alle Details findest du in unseren <a href=\"/policies/refund-policy\">Rückerstattungsrichtlinien</a>.</p>")},"block_order":["acc_ret_t"]}},
  "block_order":["acc_ship","acc_ret"]}
order=det['block_order']
print('before',order)
# order: header group, divider, variant picker, kiwi, buy buttons, sales points, payment icons, description, accordion
new=[]
for b in order:
    if b.startswith('buy_buttons'): new+=['kiwi_size',b,'sales_points','pay_icons']
    elif b.startswith('text_') and 'description' in json.dumps(det['blocks'][b]): new+=[b,'info_acc']
    else: new.append(b)
det['block_order']=new; print('after',new)
rec=p['sections'].get('product_recommendations_qggXJq'); print(json.dumps(rec)[:600])
parts=json.load(open('parts.json'))
p['sections']['about_db']=parts['about']; p['order'].append('about_db')
json.dump(p,open('product.json','w'),ensure_ascii=False,indent=1)
# about page
ia=load(I+'templates/page.about.json')
rt=ia['sections']['rich-text']['blocks']['text']['settings']['text']
tc=ia['sections']['text-columns']
about={"sections":{"about_main":{"type":"section","name":"Über uns","settings":{"content_direction":"column","horizontal_alignment_flex_direction_column":"center","gap":20,"section_width":"page-width","color_scheme":"scheme-1","padding-block-start":56,"padding-block-end":40},
   "blocks":{"ab_h":text("<h1>Über uns</h1>",'h2','center'),"ab_t":{"type":"text","settings":{"text":rt,"type_preset":"rte","alignment":"center","width":"100%","max_width":"narrow"}}},"block_order":["ab_h","ab_t"]}},"order":["about_main"]}
cols=[]
for k in tc['block_order']:
    s=tc['blocks'][k]['settings']; cols.append((k,s))
cb={}
for k,s in cols:
    bl={}; bo=[]
    if s.get('image'): bl[k+'_img']={"type":"image","settings":{"image":s['image']}}; bo.append(k+'_img')
    bl[k+'_h']=text(f"<h3>{s.get('title','')}</h3>",'h4','center'); bo.append(k+'_h')
    bl[k+'_t']=text(s.get('text',''),'rte','center'); bo.append(k+'_t')
    cb[k]={"type":"group","settings":{"content_direction":"column","horizontal_alignment_flex_direction_column":"center","gap":12,"width":"fill","width_mobile":"fill"},"blocks":bl,"block_order":bo}
about['sections']['about_cols']={"type":"section","name":"Werte","settings":{"content_direction":"row","vertical_on_mobile":True,"gap":32,"section_width":"page-width","color_scheme":"scheme-1","padding-block-start":24,"padding-block-end":56},"blocks":cb,"block_order":list(cb)}
about['order'].append('about_cols')
json.dump(about,open('page.about.json','w'),ensure_ascii=False,indent=1)
print([ (k,s.get('title')) for k,s in cols])
