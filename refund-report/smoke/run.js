const {JSDOM}=require('jsdom'); const fs=require('fs'); const d3=require('d3');
const html=fs.readFileSync('../page2/index.html','utf8');
const dir='../data_all/';
function parseCSV(t){const rows=[];let row=[],f='',q=false;for(let i=0;i<t.length;i++){const c=t[i];if(q){if(c=='"'){if(t[i+1]=='"'){f+='"';i++}else q=false}else f+=c}else if(c=='"')q=true;else if(c==','){row.push(f);f=''}else if(c=='\n'){row.push(f);rows.push(row);row=[];f=''}else if(c!='\r')f+=c}if(f.length||row.length){row.push(f);rows.push(row)}const h=rows[0];return rows.slice(1).filter(r=>r.length==h.length).map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]])))}
const ids=['stores','kpi','daily','monthly','cuts','reasons','split','payouts','coverage','exceptions','actions','qc','cases','products'];
const data={};ids.forEach(i=>data[i]=parseCSV(fs.readFileSync(dir+i+'.csv','utf8')));
const dom=new JSDOM('<!doctype html><body><div id="dash-root"></div></body>',{runScripts:'outside-only',pretendToBeVisual:true});
const w=dom.window;
const body=html.replace(/<style>[\s\S]*?<\/style>/,'');
const markup=body.replace(/<script>[\s\S]*<\/script>/,''); const script=body.match(/<script>([\s\S]*)<\/script>/)[1];
w.document.getElementById('dash-root').innerHTML=markup;
let cb=null;
w.dash={data:id=>({status:'ok',data:data[id],columns:Object.keys(data[id][0])}),onData:f=>{cb=f;},colors:['#1','#2','#3','#4','#5','#6','#7','#8']};
w.d3=d3;
Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return 640}});
w.SVGElement.prototype.getBoundingClientRect=()=>({left:0,top:0,width:640,height:250});
w.eval(script); const errs=[];
try{cb();}catch(e){errs.push(e.stack)}
const doc=w.document; const q=s=>doc.querySelector(s);
function report(tag){
 console.log('=== '+tag+' | errors',errs.length);
 console.log('tabs:',[...doc.querySelectorAll('#tabs .tab')].map(b=>b.textContent+(b.getAttribute('aria-pressed')=='true'?'*':'')).join(' | '));
 console.log('sub:',q('#sub').textContent); console.log('take:',q('#take').textContent);
 console.log('v-all hidden',q('#v-all').hidden,'v-store hidden',q('#v-store').hidden);
 if(!q('#v-all').hidden){console.log('ALL TABLE:');[...doc.querySelectorAll('#t-all tr')].forEach(r=>console.log('  ',[...r.children].map(c=>c.textContent).join(' | ')));}
 else{
  console.log('tiles:',[...doc.querySelectorAll('#tiles .card')].map(c=>c.textContent).join(' | '));
  console.log('split rows',doc.querySelectorAll('#c-split .row').length,'months',doc.querySelectorAll('#months details').length,'day rows',doc.querySelectorAll('#months tbody tr').length,'reasons',doc.querySelectorAll('#c-reasons .row').length,'product rows',doc.querySelectorAll('#d-product .row').length,'region rows',doc.querySelectorAll('#d-region .row').length,'country',[...doc.querySelectorAll('#d-country .lb')].map(e=>e.textContent).join(','));
  console.log('pp',doc.querySelectorAll('#t-pp tbody tr').length,'qc',doc.querySelectorAll('#t-qc tbody tr').length,'pay',doc.querySelectorAll('#t-pay tbody tr').length,'cov',doc.querySelectorAll('#t-cov tbody tr').length,'exc',doc.querySelectorAll('#t-exc tbody tr').length,'acts',doc.querySelectorAll('#acts .act').length);
  console.log('cases rows',doc.querySelectorAll('#t-cases tbody tr').length,[...doc.querySelectorAll('#t-cases tbody tr')].slice(0,2).map(r=>[...r.children].map(c=>c.textContent).join(' | ')).join(' // '));
  console.log('split notes:',[...doc.querySelectorAll('#split-notes li')].map(e=>e.textContent).join(' // '));
  console.log('pay-note:',q('#pay-note').textContent); console.log('cb-note:',q('#cb-note').textContent); console.log('pp-note:',q('#pp-note').textContent);
  console.log('NaN/undefined:',[...doc.querySelectorAll('#v-store *')].filter(e=>!e.children.length&&/NaN|undefined|null/.test(e.textContent)).map(e=>e.textContent.slice(0,60)));
 }}
report('default'); // all
const btns=[...doc.querySelectorAll('#tabs .tab')];
for(const name of ['Daily Berlin','Davento','Niaali']){ const b=[...doc.querySelectorAll('#tabs .tab')].find(x=>x.textContent===name); try{b.click();}catch(e){errs.push(e.stack)} report(name); }
console.log('NaN parents:',[...doc.querySelectorAll('#v-store *')].filter(e=>!e.children.length&&/NaN/.test(e.textContent)).map(e=>e.parentElement.id+'/'+e.parentElement.tagName+'/'+e.parentElement.className+': '+e.parentElement.parentElement.id));
console.log('NaN rows:',[...doc.querySelectorAll('#v-store tr')].filter(r=>/NaN/.test(r.textContent)).map(r=>(r.closest('table')||{}).id+' :: '+r.textContent.slice(0,100)));
