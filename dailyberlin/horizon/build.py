import json,re,os
IMP='/home/user/daily-berlin/dailyberlin/impulse-content/'
def load(f): return json.loads(re.sub(r'^/\*.*?\*/','',open(f).read(),flags=re.S))
imp_index=load(IMP+'templates/index.json')
faq=list(imp_index['sections']['1779873008ce6fa65a']['blocks'].values())[0]['settings']
about_html=imp_index['sections']['text_and_image_zjfRD6']['settings']['text']
feats=[(v['settings']['feature_title'],v['settings']['feature_text']) for v in imp_index['sections']['ss_feature_1_9YBKgz']['blocks'].values()]
def text(t,preset='rte',align='left',extra=None):
    s={"text":t,"type_preset":preset,"alignment":align,"width":"100%"}
    if extra: s.update(extra)
    return {"type":"text","settings":s}
def group(blocks,settings):
    return {"type":"group","settings":settings,"blocks":{k:v for k,v in blocks},"block_order":[k for k,_ in blocks]}
def sec(typ,blocks,settings,name=None):
    d={"type":typ,"blocks":{k:v for k,v in blocks},"block_order":[k for k,_ in blocks],"settings":settings}
    if name: d["name"]=name
    return d
# ---- trust row (3 features) as a reusable section
def trust_section():
    icons=['truck','return','chat_bubble']
    cols=[]
    for i,((t,h),ic) in enumerate(zip(feats,icons)):
        cols.append((f"feat_{i}",group([
            (f"feat_{i}_icon",{"type":"icon","settings":{"icon":ic,"width":32}}),
            (f"feat_{i}_title",text(f"<p><strong>{t}</strong></p>",'h5','center')),
            (f"feat_{i}_text",text(h,'rte','center')),
        ],{"content_direction":"column","horizontal_alignment_flex_direction_column":"center","gap":8,"width":"fill","width_mobile":"fill","padding-block-start":16,"padding-block-end":16,"padding-inline-start":12,"padding-inline-end":12})))
    return sec("section",cols,{"content_direction":"row","vertical_on_mobile":True,"gap":16,"section_width":"page-width","color_scheme":"scheme-1","padding-block-start":40,"padding-block-end":40},"Vorteile")
# ---- FAQ section
def faq_section():
    rows=[]
    for i in range(1,6):
        q=faq.get(f'question_{i}'); a=faq.get(f'answer_{i}')
        if q: rows.append((f"faq_row_{i}",{"type":"_accordion-row","settings":{"heading":q},"blocks":{f"faq_ans_{i}":text(a)},"block_order":[f"faq_ans_{i}"]}))
    acc={"type":"accordion","settings":{"icon":"plus","dividers":True,"type_preset":"h6"},"blocks":{k:v for k,v in rows},"block_order":[k for k,_ in rows]}
    return sec("section",[("faq_title",text("<h2>Häufig gestellte Fragen</h2>",'h3','center')),("faq_acc",acc)],
       {"content_direction":"column","horizontal_alignment_flex_direction_column":"center","gap":24,"section_width":"page-width","color_scheme":"scheme-1","padding-block-start":48,"padding-block-end":48},"FAQ")
def about_section():
    return {"type":"media-with-content","settings":{"media_position":"right","media_width":"medium","media_height":"auto","color_scheme":"scheme-1"},
      "blocks":{"media":{"type":"_media-without-appearance","static":True,"settings":{"image":"shopify://shop_images/Daily_Berlin_About_us.png","media_type":"image"}},
        "content":{"type":"_content-without-appearance","static":True,"settings":{"horizontal_alignment_flex_direction_column":"flex-start","vertical_alignment_flex_direction_column":"center","gap":20,"padding-block-start":48,"padding-block-end":48,"padding-inline-start":48,"padding-inline-end":48},
          "blocks":{"about_h":text("<h2>Über uns</h2>",'h3'),"about_t":text(about_html),"about_b":{"type":"button","settings":{"label":"Mehr über uns","link":"shopify://pages/uber-uns","style_class":"button"}}},
          "block_order":["about_h","about_t","about_b"]}}, "name":"Über uns"}
# ---- index
index={"sections":{},"order":[]}
def add(k,v): index["sections"][k]=v; index["order"].append(k)
add("hero_db", sec("hero",[
  ("hero_t1",text("<h1>Neue Saison, neue Styles</h1>",'h1','center')),
  ("hero_t2",text("<p>Entdecken Sie jetzt unsere aktuelle Kollektion für die laufende Saison.</p>",'rte','center')),
  ("hero_btns",group([("hero_b1",{"type":"button","settings":{"label":"Damen","link":"shopify://collections/women","style_class":"button"}}),
                      ("hero_b2",{"type":"button","settings":{"label":"Herren","link":"shopify://collections/men","style_class":"button-secondary"}})],
     {"content_direction":"row","vertical_on_mobile":False,"horizontal_alignment":"center","gap":12,"width":"fit-content","width_mobile":"fit-content"}))],
  {"media_type_1":"image","image_1":"shopify://shop_images/Daily_Berlin_Banner1.png","horizontal_alignment_flex_direction_column":"center","vertical_alignment_flex_direction_column":"center","gap":16,"section_width":"full-width","section_height":"large","color_scheme":"scheme-6","toggle_overlay":True,"overlay_color":"#00000040","overlay_style":"solid","padding-block-start":48,"padding-block-end":48},"Hero"))
add("trust_db", trust_section())
add("collections_db", {"type":"collection-list","name":"Kollektionen","settings":{"collection_list":["women","men"],"layout_type":"grid","columns":2,"mobile_columns":"1","section_width":"page-width","padding-block-start":24,"padding-block-end":24},
  "blocks":{"coll_head":{"type":"text","settings":{"text":"<h2>Kollektionen</h2>","type_preset":"h3","alignment":"center","width":"100%"}},
            "static-collection-card":{"type":"_collection-card","static":True,"settings":{"horizontal_alignment":"center","vertical_alignment":"center","placement":"on_image"},
              "blocks":{"collection-card-image":{"type":"_collection-card-image","static":True,"settings":{"image_ratio":"square"}},
                        "collection-title":{"type":"collection-title","settings":{"type_preset":"h3","alignment":"center","background":True,"background_color":"#ffffff","padding-block-start":8,"padding-block-end":8,"padding-inline-start":16,"padding-inline-end":16}}},
              "block_order":["collection-title"]}},
  "block_order":["coll_head"]})
add("about_db", about_section())
add("faq_db", faq_section())
json.dump(index,open('index.json','w'),ensure_ascii=False,indent=1)
json.dump({"trust":trust_section(),"about":about_section()},open('parts.json','w'),ensure_ascii=False)
print('ok',index['order'])
