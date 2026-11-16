const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [name, opts] of [['desktop', {viewport:{width:1366,height:900}}], ['mobile', devices['iPhone 13']]]) {
    const ctx = await b.newContext({...opts, locale:'nl-NL'});
    const p = await ctx.newPage();
    const base='https://niaali.com';
    await p.goto(base+'/nl-nl?preview_theme_id=210865717580',{waitUntil:'domcontentloaded'});
    const pj = await p.evaluate(async()=> (await fetch('/nl-nl/products.json?limit=5')).json());
    const v = pj.products.flatMap(x=>x.variants).find(v=>v.available);
    await p.evaluate(async(id)=> fetch('/nl-nl/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,quantity:1})}), v.id);
    await p.goto(base+'/nl-nl/cart?preview_theme_id=210865717580',{waitUntil:'networkidle'}).catch(()=>{});
    await p.waitForTimeout(2500);
    const txt = await p.evaluate(()=>{const el=document.querySelector('.cart-totals'); return el? el.innerText : 'NO CART TOTALS'});
    console.log(name, p.url(), '\n', txt, '\n----');
    const el = await p.$('.cart-totals');
    if (el) await el.screenshot({path:`cart-${name}.png`}); else await p.screenshot({path:`cart-${name}.png`});
    await ctx.close();
  }
  await b.close();
})();
