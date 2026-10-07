# Fashionnovo (www.fashionnovo.com) – analysis before the kit (2026-10-07, no changes made)

- Shop qmceit-kh, United Kingdom only, GBP, English only. 173 active / 1 draft products, inventory tracked (none at 0).
- Live theme "Horizon" 4.1.1 #198771376468 (only theme, no copy yet). Many AI-generated blocks (ai_gen_block_*).
  Fonts Tenor Sans (headings) + Outfit (body), black/white palette, radius 14 buttons, cart drawer (auto open, note open).
- theme-orig/: exact copies of the live files used for this analysis.
- Discounts: none. Shipping: "Free Shipping", GB only. Checkout: Shop Pay, PayPal, Google Pay, card (+2), Klarna, PayPal.
  Marketing checkbox "Email me with news and offers" is pre-ticked.
- Policies (Shopify policies, English): free UK shipping, processing 1–3 + transit 3–8 = 4–11 business days, cut-off 5 PM
  Mon–Sat; 60-day returns, customer pays return shipping, no restocking fee, refund within 7 business days, exchanges yes.
  Support support@fashionnovo.com, Mon–Fri 8–5, Sat–Sun 9–4 (UK), reply within 12 hours. 148-A Wandsworth Road, London.

## Issues found
1. Old brand "Labelique" in privacy policy, terms (operator name, many times), About page ("Behind Labelique"),
   empty mailto:support@labelique.com anchors (refund, FAQ, withdrawal). About page image is "Davento-about-us.png"
   with Italian alt text; homepage about image file "Labelique-about-us.png".
2. Email links href="support@fashionnovo.com" without mailto (broken) on all policies and pages.
3. "Our Collection" (menu + hero "Shop Now") has 0 products; homepage product list points to a non-existing
   collection (skirts-and-dresses) → hidden. Menu "Skirts and Dresses" → handle tops-and-shirts (3 products).
   Small sub collections: Hoodies 1, Men Accessories 1, Sleepwear 1, Jumpsuits 1, Tops & Blouses 2, Shorts 2, Trousers 2, Suits 2.
4. Withdrawal page (handle modulo-di-recesso) cites "European" rules and says withdrawal is not possible while in transit
   (UK Consumer Contracts Regulations: cancellation right runs from order until 14 days after delivery).
5. Payment lists differ: FAQ (Visa, MC, Maestro, Amex, Apple/Google/Shop Pay, UnionPay, no PayPal/Klarna) vs Payments page
   ("MasterCard, Master", + PayPal, Klarna) vs checkout. Italian page handles (chi-siamo, domande-frequenti, pagamenti).
6. Announcement "60-day money back guarantee" while the customer pays return shipping → "60-day returns" is safer.
7. Older products: flat £50/£100, 2 images, boots with option "Shoe size" XS–XL. Newer products have ~20% compare-at ("Sale").
8. Pre-ticked marketing consent in checkout (UK GDPR/PECR: consent must be opt-in).

## Done (2026-10-07, after GO)
- Automatic discounts: Buy 2, save 10% (2358642901332) · Buy 3, save 15% (2358642934100) · Buy 4+, save 20% (2358642966868).
- Main menu (quick-links): "Our Collection" (empty) removed, rest unchanged.
- Compare-at: 59 → 51 of 173 active products (29%). Removed from the 8 lowest-selling sale items in Women Jackets
  (backup with old compare-at prices: compare-at-removed.json).
- Pages (pageUpdate): contact, withdrawal (modulo-di-recesso), about (chi-siamo), FAQ (domande-frequenti), payments
  (pagamenti): mailto links, Labelique → Fashionnovo, empty Labelique links removed, payment list = checkout,
  "(UK time)", withdrawal section rewritten for the UK (14-day legal right from order + 60 days from delivery).
  About image copied from the Davento CDN to Fashionnovo Files (fashionnovo-about-us.png). Originals: orig-texts/.
- Policies: no write_legal_policies scope → corrected texts in policies/*.html to paste in Settings → Policies.
- Work theme "Fashionnovo - kit (werk)" #205357056340 (copy of live, unpublished).
