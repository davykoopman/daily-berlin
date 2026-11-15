import json,re
IMP='/home/user/daily-berlin/dailyberlin/impulse-content/'
d=json.loads(re.sub(r'/\*.*?\*/','',open(IMP+'config/settings_data.json').read(),flags=re.S))['current']['sections']
info=d['footer']['blocks']['custom_etbeJg']['settings']['text']
nl=d['footer']['blocks']['1494292487693']['settings']
ann=d['header']['blocks']['1524770292306']['settings']['text']
def text(t,preset='rte',align='left'): return {"type":"text","settings":{"text":t,"type_preset":preset,"alignment":align,"width":"100%"}}
def group(blocks,st): return {"type":"group","settings":st,"blocks":dict(blocks),"block_order":[k for k,_ in blocks]}
col={"content_direction":"column","horizontal_alignment_flex_direction_column":"flex-start","vertical_alignment_flex_direction_column":"flex-start","gap":12,"width":"fill","width_mobile":"fill"}
header={"type":"header","name":"Header","sections":{
 "header_announcements_9jGBFp":{"type":"header-announcements","name":"t:names.announcement_bar","blocks":{"announcement_BxgCk9":{"type":"_announcement","settings":{"text":ann,"link":"","font_size":"0.875rem","case":"none"}}},"block_order":["announcement_BxgCk9"],
   "settings":{"speed":5,"section_width":"page-width","color_scheme":"scheme-5","divider_width":0,"padding-block-start":10,"padding-block-end":10}},
 "header_section":{"type":"header","blocks":{
   "header-logo":{"type":"_header-logo","static":True,"settings":{"hide_logo_on_home_page":False}},
   "header-menu":{"type":"_header-menu","static":True,"settings":{"menu":"main-menu-1","type_font_primary_size":"0.875rem","menu_font_style":"inverse","type_font_primary_link":"body","type_case_primary_link":"uppercase","menu_style":"featured_products","image_border_radius":0,"navigation_bar":False,"drawer_accordion":True,"drawer_accordion_expand_first":False,"drawer_dividers":True}}},
  "settings":{"logo_position":"center","menu_position":"center","menu_row":"bottom","show_search":True,"search_position":"left","search_row":"top","show_country":False,"show_language":True,"localization_font":"body","localization_font_size":"0.875rem","localization_position":"right","localization_row":"top","section_width":"page-width","section_height":"standard","enable_sticky_header":"always","divider_width":1,"divider_size":"page-width","border_width":0,"color_scheme_top":"scheme-1","color_scheme_bottom":"scheme-1","color_scheme_transparent":"scheme-6","enable_transparent_header_home":False,"enable_transparent_header_product":False,"enable_transparent_header_collection":False}}},
 "order":["header_announcements_9jGBFp","header_section"]}
footer={"type":"footer","name":"Footer","sections":{
 "footer_m9NzUG":{"type":"footer","name":"t:names.footer","blocks":{
   "ft_info":group([("ft_info_h",text("<h3>Unsere Informationen</h3>","h6")),("ft_info_t",text(info))],col),
   "ft_menu1":{"type":"menu","settings":{"menu":"main-menu-1","heading":"Informationen","heading_preset":"h6","link_preset":"paragraph","menu_spacing":8}},
   "ft_menu2":{"type":"menu","settings":{"menu":"footer","heading":"Rechtliche Hinweise","heading_preset":"h6","link_preset":"paragraph","menu_spacing":8}},
   "ft_news":group([("ft_news_h",text("<h3>"+nl['title']+"</h3>","h6")),("ft_news_t",text(nl['text'].replace('<h3></h3>',''))),
       ("ft_news_f",{"type":"email-signup","settings":{"width":"fill","inherit_color_scheme":True,"border_style":"all","border_width":1,"border_radius":0,"display_type":"arrow","label":"Anmelden","integrated_button":True}})],col)},
  "block_order":["ft_info","ft_menu1","ft_menu2","ft_news"],
  "settings":{"section_width":"page-width","gap":40,"color_scheme":"scheme-5","padding-block-start":56,"padding-block-end":40}},
 "footer_utilities_jLGE8U":{"type":"footer-utilities","name":"t:names.utilities","blocks":{
   "footer_copyright_jweRK8":{"type":"footer-copyright","settings":{"show_powered_by":False,"font_size":"0.75rem","case":"none"}},
   "ft_pay":{"type":"payment-icons","settings":{"horizontal_alignment":"center","gap":8}},
   "social_links_Ew63Kq":{"type":"social-links","settings":{"instagram_url":"https://www.instagram.com/dailyberlin2026/"}}},
  "block_order":["footer_copyright_jweRK8","ft_pay","social_links_Ew63Kq"],
  "settings":{"section_width":"page-width","gap":24,"divider_thickness":1,"color_scheme":"scheme-5","padding-block-start":20,"padding-block-end":32}}},
 "order":["footer_m9NzUG","footer_utilities_jLGE8U"]}
json.dump(header,open('header-group.json','w'),ensure_ascii=False,indent=1)
json.dump(footer,open('footer-group.json','w'),ensure_ascii=False,indent=1)
print('ok')
