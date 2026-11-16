const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [name, opts] of [['desktop', { viewport: { width: 1366, height: 900 } }], ['mobile', devices['iPhone 13']]]) {
    const ctx = await b.newContext({ ...opts, locale: 'nl-NL' });
    const p = await ctx.newPage();
    const base = 'https://niaali.com/nl-nl';
    await p.goto(base + '?preview_theme_id=210865717580', { waitUntil: 'domcontentloaded' });
    const pj = await p.evaluate(async () => (await fetch('/nl-nl/products.json?limit=5')).json());
    const v = pj.products.flatMap(x => x.variants).find(v => v.available);
    await p.evaluate(async (id) => fetch('/nl-nl/cart/add.js', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id, quantity: 1 }) }), v.id);
    await p.goto(base + '/cart?preview_theme_id=210865717580', { waitUntil: 'networkidle' }).catch(() => {});
    await p.waitForTimeout(3000);
    const els = await p.$$('.cart-totals');
    let vis = null;
    for (const e of els) { if (await e.isVisible()) { vis = e; break; } }
    console.log(name, JSON.stringify(await vis.innerText()));
    const st = await p.evaluate(() => {
      const l = [...document.querySelectorAll('.cart-totals__total-label')].find(e => e.offsetParent);
      const s = l && getComputedStyle(l);
      const svg = [...document.querySelectorAll('.pp-cart-trust svg')].find(e => e.offsetParent);
      const vv=[...document.querySelectorAll('.cart-totals__total-value')].find(e=>e.offsetParent); const vs=vv&&getComputedStyle(vv); return { valueSize: vs&&vs.fontSize, valueWeight: vs&&vs.fontWeight, labelSize: s && s.fontSize, labelWeight: s && s.fontWeight, iconVisible: !!svg };
    });
    console.log(JSON.stringify(st));
    await vis.scrollIntoViewIfNeeded(); await vis.screenshot({ path: `cart2-${name}.png` });
    await ctx.close();
  }
  await b.close();
})();
