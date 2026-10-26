import json,glob,csv,io,os,subprocess,hashlib
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
os.makedirs('photo/img',exist_ok=True)
def load(pre):
    P=[]
    for f in sorted(glob.glob('photo/'+pre+'.*.json')):
        try:P+=json.load(open(f))['products']
        except:pass
    return {p['title'].strip().lower():p for p in P}
S={'Davento':load('dav'),'Daily Berlin':load('db'),'Niaali':load('ni')}
R=list(csv.DictReader(open('data_all/products.csv')))
items=[]
for r in R:
    p=S[r['store']].get(r['product'].strip().lower())
    if p: items.append((r['store'],r['product'],p))
def fetch(u):
    fn='photo/img/'+hashlib.md5(u.encode()).hexdigest()+'.jpg'
    if not os.path.exists(fn):
        subprocess.run(['curl','-sSL','-m','40','-o',fn,u.split('?')[0]+'?width=160'],check=False)
    return fn
def dh(fn):
    try:
        im=Image.open(fn).convert('L').resize((17,16),Image.LANCZOS);px=list(im.getdata());b=0
        for y in range(16):
            for x in range(16):
                b=(b<<1)|(px[y*17+x]>px[y*17+x+1])
        return b
    except Exception: return None
jobs=[(s,t,u['src']) for s,t,p in items for u in p['images'][:4]]
with ThreadPoolExecutor(16) as ex: files=list(ex.map(lambda j:fetch(j[2]),jobs))
H={}
for (s,t,u),fn in zip(jobs,files):
    h=dh(fn)
    if h is not None:H.setdefault((s,t),[]).append(h)
json.dump({f'{s}|{t}':v for (s,t),v in H.items()},open('photo/hashes.json','w'))
print(len(H),'products hashed of',len(items))
