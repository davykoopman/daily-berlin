# Alove Fashion (alovefashion.com) – analysis before the kit

- Live theme: "Horizon" #198978666843 (Horizon family, color_palette like Dwell/NewMae → NewMae kit ports almost 1:1).
- Market: United Kingdom only, GBP, English. Taxes included. Not Plus. 327 active / 25 draft products, no stock tracking.
- Fonts: Tenor Sans (headings), Montserrat 600 (body). Black header, black/white palette, square buttons, pill variant buttons.
- Discounts: none. Shipping: "Free Shipping" (zone "Europa" = GB) + NL zone "free".
- Checkout: card (+2), Klarna, express; shipping line "Free Shipping – Ships next business day – Track & Trace included".
- Policies are PAGES (shipping, refund, payment, terms, contact info). Shopify policy settings: only privacy (other company name/address).
  Facts: 14-day returns (customer pays return shipping unless faulty), no restocking fee, refund within 10 business days,
  exchanges possible, handling 1–2 + transit 6–9 = 7–11 business days, cut-off 5 PM GMT+00:00, support Mon–Fri 9–5, reply 1–2 business days.

## Blocking issues found
1. Menu/collections: mini/midi/maxi dress collections only contain DRAFT products → empty pages; WOMEN links to empty maxi-dresses;
   ~320 active products (AW knitwear, coats, boots, men) are in no collection at all.
2. Phone links on 6 policy pages point to a claude.ai/cowork URL instead of tel:.
3. Payment policy says EUR + Visa/MC/Apple/Google/Shop Pay; store is GBP and also offers Klarna.
4. FAQ says "Returns are free of charge"; refund policy says customer pays return shipping (change of mind).
5. Shopify privacy policy names "DK Interim Management, Venray"; pages name "RVG Online, Schijndel". Refund/shipping/terms not set
   in Settings → Policies → checkout footer only shows Privacy policy.
6. Checkout rate text "Ships next business day" contradicts policy (1–2 business days).

## Done (2026-10-03)
- Automatic discounts: Buy 2 save 10% (1939658015067), Buy 3 save 15% (1939658047835), Buy 4+ save 20% (1939658080603). Verified 2/3/4 items.
- 14 smart collections by product type created + published (womens-coats-jackets … mens-shoes-boots), plan in data/collections-plan.json.
  Meanwhile someone else built manual WOMEN/MEN + 23 manual sub collections and rebuilt main-menu → waiting for the user's choice (A keep manual / B use smart).
