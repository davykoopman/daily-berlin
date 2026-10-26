import pandas as pd, numpy as np, re, sys, os, warnings, csv
warnings.filterwarnings('ignore')
U=os.environ.get('EXPORTS_DIR','exports/').rstrip('/')+'/'
CUT=pd.Timestamp('2026-10-25'); AS_OF=pd.Timestamp('2026-10-26',tz='UTC'); TZ='Europe/Berlin'
QL='Quality issue or damaged item'; SUPL='Supplier: out of stock, color or size unavailable'
DB_LISTS=dict(
 STOCK="#1044 #1092 #1101 #1117 #1144 #1156 #1220 #1253 #1275 #1634 #1734 #1820 #1827 #1850 DB-1936 DB-1949 DB-2015 DB-2097 DB-2163 DB-2172 DB-2209 DB-2253 DB-2299 DB-2313 DB-2327".split(),
 DELAY="#1032 #1780 DB-1964".split(), ADDR="#1086 #1421 #1525 #1612".split(), THREAT="#1557 #1740 #1815 DB-1900 DB-1945 DB-2140".split(), RET=["#1149"], PRICE=["#1521"],
 Q="#1015 #1021 #1025 #1134 #1147 #1282 #1301 #1371 #1379 #1390 #1400 #1425 #1448 #1469 #1474 #1476 #1505 #1539 #1553 #1555 #1572 #1579 #1580 #1586 #1591 #1592 #1597 #1602 #1606 #1609 #1613 #1622 #1643 #1653 #1657 #1658 #1661 #1684 #1687 #1692 #1693 #1697 #1703 #1707 #1721 #1730 #1735 #1745 #1751 #1759 #1761 #1769 #1773 #1793 #1794 #1809 #1810 #1826 #1836 #1840 #1855 #1874 DB-1878 DB-1882 DB-1888 DB-1890 DB-1897 DB-1902 DB-1905 DB-1923 DB-1924 DB-1931 DB-1970 DB-1971 DB-1983 DB-2029 DB-2038 DB-2042 DB-2050 DB-2063 DB-2068 DB-2074 DB-2076 DB-2086 DB-2105 DB-2121 DB-2143 DB-2182 DB-2193 DB-2208 DB-2213 DB-2218 DB-2219 DB-2221 DB-2251 DB-2286 DB-2316".split())
DAV_LISTS=dict(STOCK="DA-1056 DA-1057 DA-1060 DA-1068 DA-1111 DA-1113 DA-1145 DA-1155 DA-1162 DA-1178 DA-1189 DA-1233".split(),DELAY=[],ADDR=[],THREAT=[],RET=[],PRICE=[],Q="DA-1054 DA-1058 DA-1078 DA-1082 DA-1101".split(),CANCEL="DA-1853 DA-1874".split(),OTHER=["DA-1897"])
STORES={
 'Daily Berlin':dict(shop='103806435677',orders='4d08ecf4-orders_export_1_95.csv',tx='c07c8989-payment_transactions_export_1_4.csv',pay='a74415fe-payouts_export_1_3.csv',domain='www.dailyberlin.de',prefixes='# and DB-',lists=DB_LISTS,post_cut=set(),manual_refund={'#1071':('2026-07-29',59.95)},not_pp={'#1699'},api_count=None,api_text='',inq=[]),
 'Davento':dict(shop='102307135831',orders='acf36c5d-orders_export_1_97.csv',tx='171901d4-payment_transactions_export_1_2.csv',pay='2197df87-payouts_export_1_4.csv',domain='www.davento.it',prefixes='# and DA-',lists=DAV_LISTS,post_cut=set(),manual_refund={},api_count=None,api_text='',inq=[('DA-1345',59.95),('DA-1458',39.95)],not_pp=set()),
 'Niaali':dict(shop='98857255244',orders='d671609a-orders_export_1_96.csv',tx='0cb27cc4-payment_transactions_export_1_3.csv',pay='02c961fd-payouts_export_1_6.csv',domain='niaali.com',prefixes='# and NI-',lists=dict(),post_cut=set(),manual_refund={},api_count=400,api_text='Live Shopify order count: 400, equal to this export.',inq=[],fx=True,not_pp={'#1009'})}
def eu(s): return pd.to_numeric(s.astype(str).str.replace('.','',regex=False).str.replace(',','.',regex=False),errors='coerce')
# ---------- shared PayPal inputs
pdx=pd.concat([pd.read_csv(U+f,encoding='utf-8-sig',low_memory=False) for f in ['cf10ef55-Download_2.CSV','335862e8-Download_4.CSV','abc99013-Download_5.CSV']]).drop_duplicates(subset=['Date','Time','Type','Transaction ID','Gross','Fee','Net','Reference Txn ID','Balance Impact']).reset_index(drop=True)
for c in ['Gross','Fee','Net']: pdx[c]=eu(pdx[c])
pdx['dt']=pd.to_datetime(pdx['Date']+' '+pdx['Time'],format='%d/%m/%Y %H:%M:%S'); pdx['day']=pdx.dt.dt.normalize()
pdx['shop']=pdx['Custom Number'].map(lambda x:(re.search(r'shop_id"+:\s*(\d+)',str(x)) or [None,None])[1])
payx=pdx[pdx.Type=='Express Checkout Payment'].drop_duplicates('Transaction ID').set_index('Transaction ID')
dis0=pd.read_csv(U+'dd2dd529-DisputesChargebacksDefault_20260101000000_20261025235959_O_01.CSV',encoding='utf-8-sig',skiprows=3,low_memory=False)
dis0=dis0[dis0['Case ID'].astype(str).str.startswith('PP-')].copy()
dis0['amt']=eu(dis0['Disputed amount']); dis0['file']=pd.to_datetime(dis0['Case filing date'],format='%Y/%m/%d %H:%M:%S')
dis0['txdt']=pd.to_datetime(dis0['Transaction Initiation Date'],format='%Y/%m/%d %H:%M:%S',utc=True).dt.tz_convert(TZ)
dis0['em']=dis0['Buyer Email Address'].str.lower(); dis0['nm']=(dis0['Buyer First Name'].fillna('')+' '+dis0['Buyer Last Name'].fillna('')).str.lower().str.strip()
dis0['shop']=dis0['Transaction ID'].map(payx.shop)
PLZ={'0':'0 Dresden / Leipzig','1':'1 Berlin / Brandenburg','2':'2 Hamburg / Bremen / N-Lower Saxony','3':'3 Hannover / Kassel','4':'4 Ruhr area / Düsseldorf','5':'5 Cologne / Bonn','6':'6 Frankfurt / Saarland','7':'7 Stuttgart / Karlsruhe','8':'8 Munich / S-Bavaria','9':'9 Nuremberg / Thuringia'}
def run(STORE,C):
    O=f'data_{STORE.split()[0].lower()}/'; os.makedirs(O,exist_ok=True)
    def out(name,df): df=df.copy(); df.insert(0,'store',STORE); df.to_csv(O+name+'.csv',index=False); return df
    SHOP=C['shop']
    # ----- orders
    raw=pd.read_csv(U+C['orders'],low_memory=False); raw['Name']=raw['Name'].ffill()
    for c in ['Email','Created at','Shipping Country','Shipping Province Name','Payment Method','Fulfilled at','Fulfillment Status','Billing Name','Shipping Name','Shipping Zip','Financial Status']: raw[c]=raw.groupby('Name')[c].transform('first')
    h=raw[raw.Total.notna()].drop_duplicates('Name').copy()
    nums=sorted(int(re.search(r'(\d+)',n).group(1)) for n in h.Name); miss=[x for x in range(nums[0],nums[-1]+1) if x not in set(nums)]
    h['dt']=pd.to_datetime(h['Created at'],utc=True).dt.tz_convert(TZ); h['day']=h.dt.dt.tz_localize(None).dt.normalize()
    n_export=len(h); last_order=h.day.max(); h_full=h.copy(); h=h[h.day<=CUT].copy()
    h['email']=h.Email.str.lower(); h['total']=h.Total.astype(float); h['ref']=h['Refunded Amount'].fillna(0).astype(float)
    h['ful']=h['Fulfilled at'].notna()
    li=raw[raw['Lineitem name'].notna()&raw.Name.isin(h.Name)].copy(); li['val']=li['Lineitem quantity']*li['Lineitem price']; li['unf']=li['Lineitem fulfillment status']!='fulfilled'
    h['unf_lines']=h.Name.map(li.groupby('Name').unf.sum()).fillna(0); h['not_shipped']=(~h.ful)|(h.unf_lines>0)
    h['channel']=np.where(h['Payment Method'].str.contains('PayPal',na=False),'PayPal','Shopify Payments')
    h.loc[h.Name.isin(C.get('not_pp',set())),'channel']='Other'
    h['plz']=h['Shipping Zip'].astype(str).str.replace("'",'').str.extract(r'(\d{5})')[0].str[0]
    # ----- Shopify Payments transactions
    t0=pd.read_csv(U+C['tx']); t0['Order']=t0.Order.astype(str)
    t0['dt']=pd.to_datetime(t0['Transaction Date'],utc=True).dt.tz_convert(TZ); t0['day']=t0.dt.dt.tz_localize(None).dt.normalize()
    t=t0[t0.day<=CUT].copy()
    if C.get('fx'):
        chg=t0[t0.Type=='charge'].groupby('Order').Amount.sum(); r_=h.Name.map(chg)/h.Total.astype(float); h['fx']=r_.fillna(r_.median()); h['total']=h.Total.astype(float)*h.fx; h['ref']=h.ref*h.fx
    meth=t0[t0.Type=='charge'].drop_duplicates('Order').set_index('Order')['Payment Method Name']
    h['method']=np.where(h.channel=='PayPal','PayPal',h.Name.map(meth).map(lambda x:'Other' if pd.isna(x) else {'klarna':'Klarna','card':'Card','twint':'Twint','satispay':'Satispay','blik':'BLIK'}.get(x,str(x).replace('_',' ').title())))
    # ----- PayPal
    pp0=pdx[(pdx.shop==SHOP)&(pdx['Balance Impact'].isin(['Credit','Debit']))].copy()
    refs={}
    for _,r in h_full.iterrows():
        for c in ['Payment Reference','Payment ID']:
            if pd.notna(r[c]): refs[str(r[c])]=r['Name']
    pp0['order']=pp0['Invoice Number'].map(refs).fillna(pp0['Reference Txn ID'].map(payx['Invoice Number'].map(refs)))
    pp=pp0[pp0.day<=CUT].copy()
    # ----- disputes
    dall=dis0[(dis0.shop==SHOP)].copy(); dis=dall[dall.file.dt.normalize()<=CUT].copy()
    dis['order']=dis['Transaction ID'].map(payx['Invoice Number'].map(refs))
    for i,r in dis.iterrows():
        if pd.notna(dis.at[i,'order']): continue
        c=h[h.email==r.em]
        if len(c): dis.at[i,'order']=c.iloc[0].Name
    dall['order']=dall['Transaction ID'].map(payx['Invoice Number'].map(refs))
    oa=dall[dall['Case status']!='Case Closed'].copy()
    cs=pd.DataFrame({'case_id':oa['Case ID'],'filed_date':oa.file.dt.strftime('%Y-%m-%d'),'reason':oa['Case reason'],'status':oa['Case status'].str.replace("Waiting For Seller's Response",'Waiting for your response'),'amount':oa.amt,'order':oa.order,'response_due':pd.to_datetime(oa['Response due date'],format='%Y/%m/%d %H:%M:%S',errors='coerce').dt.strftime('%Y-%m-%d').fillna(''),'in_report':np.where(oa.file.dt.normalize()<=CUT,'Yes','After cut-off date')})
    cs['_s']=cs.status.map({'Waiting for your response':0,'Being Reviewed By PayPal':1}).fillna(2); cs=cs.sort_values(['_s','filed_date']).drop(columns='_s'); out('cases',cs)
    # ----- reasons
    cat={}
    L=C['lists']
    for k,lab in [('STOCK',SUPL),('DELAY','Supplier: delayed or not shipped on time'),('ADDR','Customer unreachable or address problem'),('THREAT','Dispute or legal threat'),('RET','Returned to sender'),('PRICE','Pricing error'),('Q',QL),('CANCEL','Order canceled'),('OTHER','Other note')]:
        for n in L.get(k,[]): cat[n]=lab
    h['reason']=h.Name.map(cat).astype(object)
    # ----- refunds
    pp_ref_g=-pp[pp.Type=='Payment Refund'].groupby('order').Gross.sum()
    sp_ref=-t[t.Type=='refund'].groupby('Order').Amount.sum()
    sp_ref_all=-t0[t0.Type=='refund'].groupby('Order').Amount.sum(); pp_ref_all=-pp0[pp0.Type=='Payment Refund'].groupby('order').Gross.sum()
    h['sp_ref']=h.Name.map(sp_ref).fillna(0); h['pp_ref']=h.Name.map(pp_ref_g).fillna(0); h['proc']=h.sp_ref+h.pp_ref
    h['proc_all']=h.Name.map(sp_ref_all).fillna(0)+h.Name.map(pp_ref_all).fillna(0)
    h['pp_only']=(h.ref==0)&(h.pp_ref>0)
    base=np.where(h.proc_all>0,h.proc,h.ref); h['refund_eur']=np.where(h.Name.isin(C['post_cut']),0,base)
    h.loc[(h.refund_eur>0)&h.reason.isna(),'reason']='No reason entered yet'; h.loc[h.pp_only,'reason']='Refunded in PayPal, not recorded in Shopify'
    h['refd']=h.refund_eur>0; h['full']=h.refd&(h.refund_eur>=h.total-0.01); h['ns_ref']=h.refd&h.not_shipped
    h['supplier']=h.refd&(h.reason.fillna('').str.startswith('Supplier')|h.not_shipped)
    cb=t.groupby('Order').apply(lambda g: pd.Series({'cb_amt':-g[g.Type=='chargeback'].Amount.sum(),'cb_fee':g[g.Type=='chargeback'].Fee.sum()}))
    if len(cb): h=h.merge(cb,left_on='Name',right_index=True,how='left')
    else: h['cb_amt']=0.0; h['cb_fee']=0.0
    h['cb_amt']=h.cb_amt.fillna(0); h['cb_fee']=h.cb_fee.fillna(0); h['sp_cb']=h.cb_amt>0
    dd=dis.dropna(subset=['order']).drop_duplicates('order').set_index('order'); h['pp_case']=h.Name.isin(dd.index)
    h['dispute']=h.sp_cb|h.pp_case; h['prob']=h.refd|h.dispute
    rev=h.total.sum(); N=len(h)
    # ----- daily
    days=pd.date_range(h.day.min(),CUT); D=pd.DataFrame(index=days)
    D['orders']=h.groupby('day').size(); D['revenue']=h.groupby('day').total.sum()
    nsmap=h.set_index('Name').not_shipped
    tr=t[t.Type=='refund'].copy(); tr['ns']=tr.Order.map(nsmap); pr=pp[pp.Type=='Payment Refund'].copy(); pr['ns']=pr.order.map(nsmap)
    D['refund_card']=-tr.groupby('day').Amount.sum(); D['refund_paypal']=-pr.groupby('day').Gross.sum()
    D['refund_manual']=0.0; mref=0.0
    for o_,(dte,amt) in C['manual_refund'].items(): D.loc[pd.Timestamp(dte),'refund_manual']+=amt
    D['refund_not_shipped']=(-tr[tr.ns==True].groupby('day').Amount.sum()).reindex(D.index).fillna(0)+(-pr[pr.ns==True].groupby('day').Gross.sum()).reindex(D.index).fillna(0)
    if 'manual_ns' in C: D['refund_not_shipped']+=D.refund_manual
    elif C['manual_refund']: D['refund_not_shipped']+=D.refund_manual
    D['chargebacks']=-t[t.Type=='chargeback'].groupby('day').Amount.sum()
    D['chargeback_fees']=t[t.Type=='chargeback'].groupby('day').Fee.sum().reindex(D.index).fillna(0)-t[t.Type=='adjustment'].groupby('day').Amount.sum().reindex(D.index).fillna(0)
    won=t[t.Type.isin(['chargeback won','dispute_reversal'])].copy(); won['v']=won.Amount-won.Fee.where(won.Type=='chargeback won',0); D['won_back']=won.groupby('day').v.sum()
    D['paypal_lost']=-pp[pp.Type=='Payment Reversal'].groupby('day').Gross.sum(); D['paypal_fees']=-pp[pp.Type=='Dispute Fee'].groupby('day').Net.sum()
    D['refund_events']=tr.groupby('day').size().reindex(D.index).fillna(0)+pr.groupby('day').size().reindex(D.index).fillna(0)+(D.refund_manual>0)
    D['chargeback_events']=t[t.Type=='chargeback'].groupby('day').size(); D=D.fillna(0)
    D['refund_total']=D.refund_card+D.refund_paypal+D.refund_manual; D['refund_shipped']=D.refund_total-D.refund_not_shipped
    D['lost_total']=D.refund_total+D.chargebacks+D.chargeback_fees+D.paypal_lost+D.paypal_fees-D.won_back
    act=(D[['refund_total','chargebacks','chargeback_fees','won_back','paypal_lost','paypal_fees','orders']].abs().sum(axis=1)>0)
    D=D[act].round(2); D.index.name='day'; D=D.reset_index(); D['day']=D.day.dt.strftime('%Y-%m-%d')
    D['lost_rate_day']=np.where(D.revenue>0,(D.lost_total/D.revenue.replace(0,np.nan)).round(4),np.nan)
    D['revenue_cum']=D.revenue.cumsum().round(2); D['lost_cum']=D.lost_total.cumsum().round(2); D['lost_rate_cum']=(D.lost_cum/D.revenue_cum.replace(0,np.nan)).round(4)
    D=D[['day','orders','revenue','refund_card','refund_paypal','refund_manual','refund_total','refund_not_shipped','refund_shipped','chargebacks','chargeback_fees','won_back','paypal_lost','paypal_fees','lost_total','refund_events','chargeback_events','lost_rate_day','revenue_cum','lost_cum','lost_rate_cum']]
    out('daily',D); tot=D.drop(columns='day').sum(numeric_only=True)
    D['month']=D.day.str[:7]; M=D.groupby('month').sum(numeric_only=True).reset_index().drop(columns=['lost_rate_day','revenue_cum','lost_cum','lost_rate_cum']); M['lost_rate']=(M.lost_total/M.revenue.replace(0,np.nan)).round(4); out('monthly',M.round(2))
    # ----- cuts
    def agg(df,dim,col):
        g=df.groupby(col).agg(orders=('Name','size'),revenue=('total','sum'),refund_orders=('refd','sum'),refund_eur=('refund_eur','sum'),refund_full=('full','sum'),not_shipped_refund_eur=('refund_eur',lambda s:s[df.loc[s.index,'ns_ref']].sum()),dispute_orders=('dispute','sum'),problem_orders=('prob','sum'),sp_chargebacks=('sp_cb','sum'),pp_cases=('pp_case','sum')).reset_index().rename(columns={col:'label'}); g.insert(0,'dimension',dim); return g
    P=[agg(h[h.method!='Other'],'Payment method','method')]
    cc=h['Shipping Country'].value_counts(); h['country']=h['Shipping Country'].where(h['Shipping Country'].map(cc)>=10,'Other'); P.append(agg(h,'Country','country'))
    def region(r):
        c=r['Shipping Country']
        if c=='DE' and pd.notna(r.plz): return 'DE '+PLZ[r.plz]
        if c=='IT': return 'IT '+str(r['Shipping Province Name']) if pd.notna(r['Shipping Province Name']) else 'IT (unknown)'
        if c=='AT' and STORE=='Daily Berlin' and pd.notna(r.plz): return PLZ[r.plz]
        return c if pd.notna(c) else 'Unknown'
    if STORE=='Daily Berlin':
        h['region']=np.where(h.plz.notna(),h.plz.map(PLZ),None)
    else:
        h['region']=h.apply(region,axis=1)
    rg=h[h.region.notna()]; A=agg(rg,'Region','region'); 
    if STORE!='Daily Berlin':
        small=A[A.orders<20].label.tolist(); rg2=rg.copy(); rg2['region']=rg2.region.where(~rg2.region.isin(small),np.where(rg2.region.str.startswith('IT '),'IT other provinces',np.where(rg2.region.str.startswith('DE '),'DE other','Other'))); A=agg(rg2,'Region','region')
    P.append(A)
    bands=[(0,30,'up to €30'),(30,45,'€30–45'),(45,60,'€45–60'),(60,80,'€60–80'),(80,100,'€80–100'),(100,150,'€100–150'),(150,1000,'over €150')]
    h['band']=pd.cut(h.total,[b[0] for b in bands]+[1000],labels=[b[2] for b in bands]).astype(str); P.append(agg(h,'Order value','band'))
    h['ship']=np.where(h.not_shipped,'Not (fully) shipped','Shipped'); P.append(agg(h,'Shipping status','ship'))
    Lx=li.merge(h[['Name','total','refund_eur','dispute','sp_cb','pp_case','refd','ns_ref','prob','reason']],on='Name'); Lx['share']=Lx.val/Lx.groupby('Name').val.transform('sum')
    unf_val=Lx[Lx.unf].groupby('Name').val.sum(); Lx['ns_share']=np.where(Lx.unf&Lx.ns_ref,Lx.val/Lx.Name.map(unf_val).replace(0,np.nan),0)
    Lx['ref_alloc']=Lx.refund_eur*Lx.share; Lx['ns_alloc']=Lx.refund_eur*Lx.ns_share.fillna(0)
    Lx['prod']=Lx['Lineitem name'].str.replace(r'\s*-\s*[^-]*$','',regex=True).str.strip()
    LF=Lx.drop_duplicates(['Name','prod']).groupby('prod').agg(orders=('Name','nunique'),refund_orders=('refd','sum'),dispute_orders=('dispute','sum'),problem_orders=('prob','sum'),sp_chargebacks=('sp_cb','sum'),pp_cases=('pp_case','sum'))
    LM=Lx.groupby('prod').agg(revenue=('val','sum'),refund_eur=('ref_alloc','sum'),not_shipped_refund_eur=('ns_alloc','sum'))
    pg=LF.join(LM).reset_index().rename(columns={'prod':'label'}); pg['refund_full']=0; pg=pg[pg.orders>=20].sort_values('problem_orders',ascending=False).head(14); pg.insert(0,'dimension','Product'); P.append(pg)
    Cc=pd.concat(P); Cc['refund_rate']=Cc.refund_orders/Cc.orders; Cc['dispute_rate']=Cc.dispute_orders/Cc.orders; Cc['problem_rate']=Cc.problem_orders/Cc.orders
    for c in ['revenue','refund_eur','not_shipped_refund_eur']: Cc[c]=Cc[c].round(2)
    for c in ['refund_rate','dispute_rate','problem_rate']: Cc[c]=Cc[c].round(4)
    out('cuts',Cc)
    # ----- reasons
    rf=h[h.refd]; R=[]
    for r,g in rf.groupby('reason'): R.append(['Refund reason',r,len(g),round(g.refund_eur.sum(),2),int(g.ns_ref.sum()),round(g[g.ns_ref].refund_eur.sum(),2)])
    R.append(['Refund type','Fully refunded orders',int(rf.full.sum()),round(rf[rf.full].refund_eur.sum(),2),0,0]); R.append(['Refund type','Partially refunded orders',int((~rf.full).sum()),round(rf[~rf.full].refund_eur.sum(),2),0,0])
    sup=rf[rf.supplier]; sn=rf.reason.fillna('').str.startswith('Supplier')
    R.append(['Supplier issue','Refunded: noted as supplier issue',int(sn.sum()),round(rf[sn].refund_eur.sum(),2),0,0]); R.append(['Supplier issue','Refunded: never (fully) shipped',int(rf.ns_ref.sum()),round(rf[rf.ns_ref].refund_eur.sum(),2),0,0]); R.append(['Supplier issue','Either of the two (no double count)',len(sup),round(sup.refund_eur.sum(),2),0,0])
    for k,col in [('PayPal case reason','Case reason'),('PayPal case status','Case status'),('PayPal outcome','Outcome'),('PayPal case type','Case type'),('PayPal outcome reason','Final Outcome Reason')]:
        for r,g in dis.groupby(dis[col].fillna('No outcome yet')): R.append([k,r,len(g),round(g.amt.sum(),2),0,0])
    for (rs_,oc),g in dis.groupby([dis['Case reason'],dis['Outcome'].fillna('Open')]): R.append(['PayPal reason and outcome',f'{rs_}: {oc}',len(g),round(g.amt.sum(),2),0,0])
    txt=dis['Buyer comments'].fillna('').str.lower()
    themes={'Product comes from China or long delivery':'china|cina|lieferzeit|aus china|verspät|wochen|noch nicht|nicht erhalten|nicht angekommen|nie angekommen|ritardo|non è arrivat|non arrivat|mai arrivat|settimane|consegna','Quality or material':'qualität|material|stoff|leinen|billig|qualità|tessuto|scadente|materiale','Photo or description does not match':'foto|bild|beschreib|abgebildet|anders aus|nicht wie|descrizione|diverso|non corrisponde|immagin','Size or fit':'größe|zu klein|zu groß|passt|grösse|taglia|misura|piccol|grande'}
    for k,v in themes.items(): R.append(['Customer comment theme',k,int(txt.str.contains(v).sum()),0,0,0])
    sp=h[h.sp_cb]
    for m,g in sp.groupby('method'): R.append(['Shopify chargebacks by method',m,len(g),round(g.cb_amt.sum(),2),0,0])
    Rd=pd.DataFrame(R,columns=['kind','label','orders','eur','not_shipped_orders','not_shipped_eur']); Rd['share_of_refunds']=np.where(Rd.kind.isin(['Refund reason','Refund type','Supplier issue']),(Rd.eur/max(tot.refund_total,0.01)).round(4),np.nan); out('reasons',Rd)
    # ----- split
    ns=rf[rf.ns_ref]; sh=rf[~rf.ns_ref]; sns=lambda d:d.reason.fillna('').str.startswith('Supplier')
    known=[QL,'Dispute or legal threat','Refunded in PayPal, not recorded in Shopify']
    S=[('Refunds: never (fully) shipped','Not shipped, noted as supplier issue (stock, color, size)',ns[sns(ns)].refund_eur.sum()),('Refunds: never (fully) shipped','Not shipped, other (reason not entered yet)',ns[~sns(ns)].refund_eur.sum()),
    ('Refunds: shipped','Quality issue or damaged item',sh[sh.reason==QL].refund_eur.sum()),('Refunds: shipped','Supplier delay or stock issue',sh[sns(sh)].refund_eur.sum()),('Refunds: shipped','Dispute or legal threat',sh[sh.reason=='Dispute or legal threat'].refund_eur.sum()),('Refunds: shipped','Refunded in PayPal, not recorded in Shopify',sh[sh.reason=='Refunded in PayPal, not recorded in Shopify'].refund_eur.sum()),('Refunds: shipped','Other (reason not entered yet)',sh[~sh.reason.isin(known)&~sns(sh)].refund_eur.sum()),
    ('Chargebacks and disputes','Shopify Payments chargebacks (disputed amount)',D.chargebacks.sum()),('Chargebacks and disputes','Shopify Payments fee per chargeback',D.chargeback_fees.sum()),('Chargebacks and disputes','Shopify Payments money won back',-D.won_back.sum()),('Chargebacks and disputes','PayPal disputes lost',D.paypal_lost.sum()),('Chargebacks and disputes','PayPal dispute fees',D.paypal_fees.sum())]
    Sd=pd.DataFrame(S,columns=['group','label','amount']); Sd['amount']=Sd.amount.round(2); lt=Sd.amount.sum(); Sd['share_of_lost']=(Sd.amount/lt if lt else 0); Sd['share_of_lost']=Sd.share_of_lost.round(4); Sd['share_of_revenue']=(Sd.amount/rev).round(4); out('split',Sd)
    assert abs(lt-tot.lost_total)<0.02,(lt,tot.lost_total)
    # ----- expected, kpi
    spo=h[h.channel=='Shopify Payments']; ppo=h[h.channel=='PayPal']; kl=h[h.method=='Klarna']; cd=h[h.method=='Card']
    cb2=t[t.Type=='chargeback'].merge(h[['Name','dt']],left_on='Order',right_on='Name',suffixes=('','_o')); dys=((cb2['dt']-cb2['dt_o']).dt.total_seconds()/86400).values
    age=((AS_OF-h.dt.dt.tz_convert('UTC')).dt.total_seconds()/86400)
    if len(dys)>=5:
        Fn=lambda a:(dys<=a).mean(); mat=spo[age[spo.index]>=70]; p_mat=mat.sp_cb.mean() if len(mat) else 0; exp_cb=sum(p_mat*(1-Fn(a)) for a in age[spo.index] if a>=0); avg_cb=h[h.sp_cb].cb_amt.mean()
    else: exp_cb=np.nan; avg_cb=0; dys=np.array([np.nan])
    closed=dis[dis['Case status']=='Case Closed']; opn=dis[dis['Case status']!='Case Closed']; dec=closed[closed.Outcome.isin(['Win','Refund','Loss'])]
    loss_share=dec[dec.Outcome.isin(['Refund','Loss'])].amt.sum()/dec.amt.sum() if len(dec)>=10 else None
    age_d=(CUT-h.day).dt.days; openus=h[h.not_shipped&~h.refd&(age_d>7)]; recent=h[h.not_shipped&~h.refd&(age_d<=7)]
    pay=pd.read_csv(U+C['pay']); pay['pday']=pd.to_datetime(pay['Payout Date']); ta=t0.copy(); ta['pday']=pd.to_datetime(ta['Payout Date'])
    rec=pd.DataFrame({'ch':ta[ta.Type=='charge'].groupby('pday').Amount.sum(),'rf':ta[ta.Type=='refund'].groupby('pday').Amount.sum(),'adj':ta[ta.Type.isin(['chargeback','chargeback won','dispute_reversal','adjustment'])].groupby('pday').Amount.sum(),'fee':ta.groupby('pday').Fee.sum()}).fillna(0)
    m=pay.set_index('pday').join(rec).fillna(0); m['tx_total']=(m.ch+m.rf+m.adj+m['Reserved Funds']-m.fee).round(2); m['diff']=(m.Total-m.tx_total).round(2)
    payo=pd.DataFrame({'payout_date':m.index.strftime('%Y-%m-%d'),'status':m.Status.values,'new_sales':m.Charges.values,'refunds':m.Refunds.values,'chargebacks_adjustments':m.Adjustments.values,'reserve':m['Reserved Funds'].values,'fees':m.Fees.values,'total':m.Total.values,'rebuilt_from_transactions':m.tx_total.values,'unexplained':m['diff'].values}).sort_values('payout_date',ascending=False); out('payouts',payo)
    neg=m[m.Total<0]
    def sf(a,b): return round(a/b,4) if b else 0
    K=[('orders',N),('revenue',round(rev,2)),('lost_total',round(tot.lost_total,2)),('lost_rate',sf(tot.lost_total,rev)),('refund_total',round(tot.refund_total,2)),('refund_rate_eur',sf(tot.refund_total,rev)),('refund_orders',int(h.refd.sum())),('refund_order_rate',round(h.refd.mean(),4)),('refund_full_n',int(rf.full.sum())),('refund_partial_n',int((~rf.full).sum())),('refund_value_share',sf(rf.refund_eur.sum(),rf.total.sum())),
    ('ns_refund_eur',round(rf[rf.ns_ref].refund_eur.sum(),2)),('ns_refund_orders',int(rf.ns_ref.sum())),('ns_refund_share',sf(rf[rf.ns_ref].refund_eur.sum(),tot.refund_total)),('supplier_eur',round(rf[rf.supplier].refund_eur.sum(),2)),('supplier_orders',int(rf.supplier.sum())),('supplier_share',sf(rf[rf.supplier].refund_eur.sum(),tot.refund_total)),
    ('unshipped_orders',int(h.not_shipped.sum())),('open_unshipped_orders',len(openus)),('open_unshipped_eur',round(openus.total.sum(),2)),('recent_unshipped_orders',len(recent)),('recent_unshipped_eur',round(recent.total.sum(),2)),
    ('cb_eur',round(tot.chargebacks,2)),('cb_orders',int(h.sp_cb.sum())),('cb_rate',round(spo.sp_cb.mean(),4) if len(spo) else 0),('klarna_rate',round(kl.sp_cb.mean(),4) if len(kl) else 0),('card_rate',round(cd.sp_cb.mean(),4) if len(cd) else 0),('klarna_orders',len(kl)),('klarna_share_cb',sf(kl.sp_cb.sum(),h.sp_cb.sum())),
    ('pp_cases',len(dis)),('pp_rate',round(ppo.pp_case.mean(),4) if len(ppo) else 0),('pp_lost_eur',round(tot.paypal_lost,2)),('pp_open_cases',len(opn)),('pp_open_amount',round(opn.amt.sum(),2)),('pp_expected_loss',round(opn.amt.sum()*loss_share,2) if loss_share is not None else np.nan),
    ('exp_extra_cb',round(exp_cb) if exp_cb==exp_cb else np.nan),('exp_extra_cb_eur',round(exp_cb*(avg_cb+15)) if exp_cb==exp_cb else np.nan),('cb_median_days',int(np.nanmedian(dys)) if len(dys)>=5 or dys[0]==dys[0] else np.nan),('cb_after_30',round((dys>30).mean(),4) if dys[0]==dys[0] else np.nan),
    ('neg_payouts_n',len(neg)),('neg_payouts_sum',round(neg.Total.sum(),2)),('payout_unexplained',round(m['diff'].abs().sum(),2)),('dispute_orders',int(h.dispute.sum())),('dispute_rate',round(h.dispute.mean(),4)),
    ('young_order_share',round((age_d<=30).mean(),4)),('young_order_count',int((age_d<=30).sum())),('pp_open_after_cutoff',int((oa.file.dt.normalize()>CUT).sum())),('pp_awaiting_total',int((oa['Case status']=="Waiting For Seller's Response").sum())),('inquiries_open',len(C['inq'])),('inquiries_open_eur',round(sum(a for _,a in C['inq']),2))]
    labels={'orders':'Orders','revenue':'Gross revenue','lost_total':'Total lost to refunds and chargebacks','lost_rate':'Lost as share of revenue'}
    out('kpi',pd.DataFrame([(a,b,labels.get(a,a)) for a,b in K],columns=['metric','value','label']))
    # ----- coverage
    unl=pp0[(pp0.Type=='Express Checkout Payment')&(pp0['Balance Impact']=='Credit')&pp0.order.isna()&(pp0.day<=CUT)]
    dt_=lambda x:'' if pd.isna(x) else pd.Timestamp(x).strftime('%Y-%m-%d')
    pend=ta[~ta.pday.isin(pay.pday)]
    cov=[('Shopify orders (export)',dt_(h.day.min()),dt_(last_order),n_export,'OK' if not miss else 'Check',(f'Order numbers {nums[0]} to {nums[-1]} are continuous with no gaps. '+C['api_text']+f' The report stops at {CUT:%d %B %Y}, so later orders are left out.') if not miss else f'Missing order numbers: {miss[:10]}'),
    ('Shopify Payments transactions',dt_(t0.day.min()),dt_(t0.day.max()),len(t0),'OK','Every order in the transactions exists in the order export. Transactions after the cut-off date are excluded from the report.'),
    ('Shopify Payments payouts',dt_(pay.pday.min()),dt_(pay.pday.max()),len(pay),'OK' if m['diff'].abs().sum()==0 else 'Check',f'{len(pay)} payouts rebuilt from transactions, total unexplained difference {m["diff"].abs().sum():.2f}.'+(f' {len(pend)} transactions belong to payouts not yet in the export (pending).' if len(pend) else '')),
    ('PayPal transactions (all stores in the account)',dt_(pdx.day.min()),dt_(pdx.day.max()),len(pdx),'OK',f'Report uses only shop {SHOP}. Rows after the cut-off date are excluded.'),
    ('PayPal payments linked to Shopify orders',dt_(pp0[pp0.Type=="Express Checkout Payment"].day.min()),dt_(pp0[pp0.Type=="Express Checkout Payment"].day.max()),int((pp0.Type=='Express Checkout Payment').sum()),'OK' if len(unl)==0 else 'Check',('This store does not use PayPal.' if pp0.empty else f'{len(unl)} payments of this store could not be linked to an order.' if len(unl) else 'Every PayPal payment of this store is linked to a Shopify order.')),
    ('PayPal cases (disputes and claims)','2026-01-01','2026-10-25',len(dall),'OK',f'{len(dis)} cases of this store were filed up to the cut-off date and {len(dall)-len(dis)} after it. All are linked to an order by transaction ID.'),
    ('Refund check: Shopify against payment providers',dt_(h.day.min()),dt_(CUT),int(h.refd.sum()),'Check','Differences are listed in the exceptions table.')]
    out('coverage',pd.DataFrame(cov,columns=['source','from_date','to_date','rows','status','note']))
    # ----- exceptions
    E=[]; pol=dd
    for r in h[h.pp_only].itertuples():
        c=pol.loc[r.Name] if r.Name in pol.index else None
        E.append((r.Name,r.day.strftime('%Y-%m-%d'),'PayPal','Refunded in PayPal, not recorded in Shopify',round(r.refund_eur,2),f"PayPal case: {c['Case reason']}, outcome {c['Outcome'] if pd.notna(c['Outcome']) else 'open'}" if c is not None else 'No PayPal case found; refund made directly in PayPal'))
    for r in h[(h.channel=='PayPal')&(h.ref>0)&((h.ref-h.pp_ref).abs()>0.005)&(h.pp_ref>0)].itertuples(): E.append((r.Name,r.day.strftime('%Y-%m-%d'),'PayPal','Shopify refund differs from PayPal refund',round(r.ref-r.pp_ref,2),f'Shopify {r.ref:.2f}, PayPal {r.pp_ref:.2f}'))
    for o_,(dte,amt) in C['manual_refund'].items(): E.append((o_,'2026-07-26','Manual order','Refund without a payment provider',amt,'Manual payment. Refund recorded in Shopify, no Shopify Payments or PayPal movement.'))
    for o_ in sorted(C['post_cut']): E.append((o_,'','Shopify Payments or PayPal','Refund made after the cut-off date',59.95,'Refunded after the cut-off date, excluded from this report.'))
    for r in openus.itertuples(): E.append((r.Name,r.day.strftime('%Y-%m-%d'),r.channel,'Paid, not shipped for more than 7 days, not refunded',round(r.total,2),f'{(CUT-r.day).days} days since the order'))
    ppref=set(pp0[pp0.Type=='Express Checkout Payment']['Invoice Number'].astype(str))
    for r in h[(h.channel=='PayPal')&~h['Payment Reference'].astype(str).isin(ppref)].itertuples():
        gap=(r.dt>=pd.Timestamp('2026-10-24 13:00',tz=TZ))&(r.dt<pd.Timestamp('2026-10-25 01:00',tz=TZ))
        E.append((r.Name,r.day.strftime('%Y-%m-%d'),'PayPal','Paid with PayPal, payment not in the PayPal export',round(r.total,2),'Falls in the gap of the PayPal export (24 Oct 13:04 to 25 Oct 00:26). Export the missing period to close it.' if (r.day>=pd.Timestamp('2026-10-24')) else 'No matching payment in the PayPal export. Check this order in PayPal.'))
    for o_,a_ in C['inq']: E.append((o_,h_full.set_index('Name').day.get(o_).strftime('%Y-%m-%d'),'Shopify Payments','Bank inquiry under review, nothing debited yet',a_,'Shopify shows a dispute that started as an inquiry. It can still turn into a chargeback plus a fee of 15 euro.'))
    out('exceptions',pd.DataFrame(E,columns=['order','order_date','channel','issue','amount','detail']))
    # ----- products with more than 3 orders and the quality check list
    q=Lx.drop_duplicates(['Name','prod']).copy()
    q['q_ref']=q.reason==QL; q['na']=q.Name.isin(dd[dd['Case reason']=='Not as described'].index)
    qa=q.groupby('prod').agg(orders=('Name','nunique'),refund_orders=('refd','sum'),quality_refund_orders=('q_ref','sum'),not_as_described_cases=('na','sum'),problem_orders=('prob','sum'))
    qe=Lx[Lx.reason==QL].groupby('prod').ref_alloc.sum(); qa['quality_refund_eur']=qe.reindex(qa.index).fillna(0).round(2)
    qa['revenue']=Lx.groupby('prod').val.sum().reindex(qa.index).round(2)
    qa['signals']=qa.quality_refund_orders+qa.not_as_described_cases; qa['problem_rate']=(qa.problem_orders/qa.orders).round(4)
    listed=(qa.orders>=10)&(qa.signals>=2)
    qa['priority']=np.where(listed,np.where((qa.signals>=5)|((qa.signals>=3)&(qa.problem_rate>=0.3)),'High','Medium'),'')
    qa['suggested_check']=np.where(qa.not_as_described_cases>=qa.quality_refund_orders,'Compare the product with the page: photos, color, size chart and description. Ask the supplier for a sample.','Ask the supplier for a quality inspection: material, stitching, damage. Ask for a sample.')
    qa.loc[qa.priority=='','suggested_check']=''
    st_file='data_all/qc_status.csv'
    stat=pd.read_csv(st_file) if os.path.exists(st_file) else pd.DataFrame(columns=['store','product','status','checked_on','note'])
    stat=stat[stat.store==STORE].set_index('product')
    qa=qa.reset_index().rename(columns={'prod':'product'})
    for col,dflt in [('status','Not checked yet'),('checked_on',''),('note','')]:
        qa[col]=qa['product'].map(stat[col]) if len(stat) else np.nan
        qa[col]=qa[col].fillna(dflt)
    prods=qa[qa.orders>3].copy(); prods['_p']=prods.priority.map({'High':0,'Medium':1}).fillna(2); prods=prods.sort_values(['_p','orders'],ascending=[True,False]).drop(columns='_p'); prods['rank']=range(1,len(prods)+1)
    out('products',prods[['rank','product','priority','orders','revenue','refund_orders','quality_refund_orders','quality_refund_eur','not_as_described_cases','problem_rate','status','checked_on','note']])
    qq=qa[qa.priority!=''].copy(); qq['_p']=qq.priority.map({'High':0,'Medium':1}); qq=qq.sort_values(['_p','signals'],ascending=[True,False]).drop(columns='_p'); qq['rank']=range(1,len(qq)+1)
    out('qc',qq[['rank','product','priority','orders','problem_rate','quality_refund_orders','quality_refund_eur','not_as_described_cases','suggested_check','status','checked_on','note']])
    qa=qq
    K.extend([('qc_products',len(prods)),('qc_checked',int((prods.status!='Not checked yet').sum())),('qc_good',int((prods.status=='Good').sum())),('qc_not_good',int((prods.status=='Not good').sum()))])
    out('kpi',pd.DataFrame([(a,b,labels.get(a,a)) for a,b in K],columns=['metric','value','label']))
    print(STORE,'orders',N,'rev',round(rev,2),'lost',round(tot.lost_total,2),'refund',round(tot.refund_total,2),'ns',round(rf[rf.ns_ref].refund_eur.sum(),2),'cb',round(tot.chargebacks,2),'cases',len(dis),'open',len(opn),'qc rows',len(qa))
    h.to_pickle(O+'h.pkl')
    return h
if __name__=='__main__':
    for s in (sys.argv[1:] or STORES): run(s,STORES[s])
