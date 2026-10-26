import pandas as pd, csv
B=''
for n in ['daily','monthly','cuts','reasons','split','payouts','coverage','exceptions','kpi','qc','cases','products']:
    a=pd.read_csv(B+f'data_daily/{n}.csv'); b=pd.read_csv(B+f'data_davento/{n}.csv'); c=pd.read_csv(B+f'data_niaali/{n}.csv'); pd.concat([a,b,c]).to_csv(B+f'data_all/{n}.csv',index=False)
print('combined')
