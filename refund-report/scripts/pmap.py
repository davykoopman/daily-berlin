import pandas as pd, re, numpy as np
U=os.environ.get('EXPORTS_DIR','exports/').rstrip('/')+'/'
def lines(f):
    o=pd.read_csv(U+f,low_memory=False); o['Name']=o['Name'].ffill(); l=o[o['Lineitem name'].notna()].copy()
    l['prod']=l['Lineitem name'].str.replace(r'\s*-\s*[^-]*$','',regex=True).str.strip(); l['col']=l['Lineitem name'].str.split(' - ').str[-1].str.split(' / ').str[0].str.strip(); return l
a=lines('11477892-orders_export_1_92.csv'); b=lines('58d46433-orders_export_1_93.csv')
def summ(x):
    g=x.groupby('prod').agg(orders=('Name','nunique'),price=('Lineitem price','median'),cols=('col',lambda s:set(s))).reset_index(); return g[g.orders>3].set_index('prod')
ga=summ(a); gb=summ(b)
CT={'grau':'grigio','khaki':'khaki','blau':'blu','braun':'marrone','beige':'beige','schwarz':'nero','weiß':'bianco','grün':'verde','rosa':'rosa','dunkelgrau':'grigio scuro','dunkelgrün':'verde scuro','burgund':'bordeaux','hellgrau':'grigio chiaro','gelb':'giallo','lila':'viola','marine':'blu navy','marineblau':'blu navy','hellblau':'azzurro','rot':'rosso','armeegrün':'verde esercito','hellbraun':'marrone chiaro'}
def norm_it(c): c=c.lower().replace('cachi','khaki'); return c
def common(ca,cb):
    cbn={norm_it(c) for c in cb}; out=[]
    for c in ca:
        t=CT.get(c.lower(),c.lower()); 
        if t in cbn or norm_it(t) in cbn: out.append(c)
    return sorted(out)
P=[('Men cargo bermuda shorts','Herren Cargo Bermudashorts für aktive Tage','Bermuda Cargo da Uomo per Giorni Attivi','High'),
('Men cargo trousers','Herren Cargohose für Freizeit und Alltag','Pantaloni cargo da uomo per il tempo libero e la vita quotidiana','High'),
('Women clogs with adjustable buckle','Damen Clogs mit verstellbarer Schnalle','Zoccoli da donna con fibbia regolabile','High'),
('Men clogs','Herren Clogs mit verstellbarer Schnalle','Zoccoli da uomo per uso quotidiano','Medium'),
('Men suit for special occasions','Herren Anzug für besondere Anlässe','Completo da uomo per occasioni speciali','High'),
('Women linen-mix blouse, elegant','Damen Leinenbluse mit Leinenmix Elegant','Blusa in Lino da Donna con Mix di Lino Elegante','High'),
('Women lace dress with open back','Damen Spitzenkleid mit Rückenöffnung','Abito in pizzo da donna con apertura sulla schiena','High'),
('Men western boots','Herren Westernstiefel für besondere Anlässe','Stivali western da uomo per occasioni speciali','High'),
('Men baggy jeans streetwear','Herren Baggy Jeans mit weitem Schnitt','Jeans Baggy da Uomo con Taglio Ampio Streetwear','Medium'),
('Men pleated wide-leg trousers','Herren Bundfaltenhose mit weitem Bein','Pantaloni da uomo con pieghe e gamba ampia','High'),
('Women loafers for office and leisure','Damen Loafer für Büro und Freizeit','Mocassini da donna per ufficio e tempo libero','High'),
('Women swimsuit','Damen Badeanzug für Strand und Badeurlaub','Abito da bagno da donna per mare e piscina','High'),
('Women blouse with floral pattern and buttons','Damen Bluse mit Blumenmuster und Knopfleiste','Blusa da donna con motivo floreale e bottoni','High'),
('Men festive suit','Herren Anzug für festliche Anlässe','Completo elegante da uomo per cerimonie e occasioni formali','High'),
('Men jacket for transitional seasons','Herrenjacke für Übergangszeit und verschiedene Anlässe','Giacca Uomo Strutturata per Stile Quotidiano e Cittadino','High'),
('Women hooded jacket','Damenjacke mit Kapuze für Alltag und Freizeit','Giacca da donna con cappuccio per la vita quotidiana e il tempo libero','High'),
('Women plaid coat, midi length','Damen Karomantel in Midilänge','Cappotto da Donna per Giornate Autunnali','High'),
('Women wide-leg jeans','Damen Jeans mit weitem Bein','Jeans Donna a Gamba Ampia per Uso Quotidiano','Medium'),
('Men slip-on sneakers','Herren Slip-on Sneaker für aktive Freizeit','Scarpe slip-on da uomo per il tempo libero','Medium'),
('Women summer sandals','Damen Sandalen für sommerliche Anlässe','Sandali Donna per Giornate Calde','Medium'),
('Women two-piece set, elegant','Damen Zweiteiler für elegante Kombinationen','Completo da Donna per Occasioni Eleganti','Medium'),
('Women two-piece set, spring and summer','Damen Zweiteiler für Frühling und Sommer','Completo da Donna per Occasioni Quotidiane','Medium'),
('Women ski jacket','Damen Skijacke für Wintersport','Giacca da Sci Donna per le Giornate Invernali','Medium'),
('Men biker jacket','Herren Bikerjacke mit Reißverschluss','Giacca Uomo in Stile Biker','Medium'),
('Men corduroy trousers','Herren Cordhose mit lockerem Schnitt','Pantaloni Uomo in Velluto a Coste per Ogni Giorno','Medium'),
('Women trench coat','Damen Trenchcoat Elegant','Trench Donna Lungo con Cintura per la Mezza Stagione','Medium'),
('Men outdoor vest','Herren Outdoor Weste für Freizeit','Gilet da uomo per attività e tempo libero','Medium'),
('Women raincoat with hood','Damen Regenmantel mit Kapuze','Giacca Donna Lunga con Cappuccio per Giornate Piovose','Medium'),
('Women sneakers with striking lacing','Damen Sneaker mit auffälliger Schnürung','Sneakers da donna dal design casual quotidiano','Medium'),
('Women pumps','Damen Pumps für festliche Anlässe','Décolleté da Donna per Occasioni Speciali','Medium')]
rows=[]; used_a=set(); used_b=set()
for en,pa,pb,conf in P:
    ma=[p for p in ga.index if p.startswith(pa)]; mb=[p for p in gb.index if p.startswith(pb)]
    if len(ma)!=1 or len(mb)!=1: print('NO UNIQUE MATCH',en,ma,mb); continue
    A,B=ga.loc[ma[0]],gb.loc[mb[0]]; cc=common(A.cols,B.cols)
    ev=('Same price €%.2f'%A.price if abs(A.price-B.price)<0.011 else 'Price €%.2f vs €%.2f'%(A.price,B.price))+('; colors in common: '+', '.join(cc) if cc else '; no color in common')
    rows.append(dict(master=en,daily_berlin_product=ma[0],db_orders=int(A.orders),davento_product=mb[0],dav_orders=int(B.orders),confidence=conf,evidence=ev)); used_a.add(ma[0]); used_b.add(mb[0])
pm=pd.DataFrame(rows); pm.to_csv('data_all/product_map.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',60)
print(pm[['master','db_orders','dav_orders','confidence','evidence']].to_string()); print(len(pm),'pairs;',pm.confidence.value_counts().to_dict())
