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

## Kit in work theme "Alove - kit (werk)" #202302062939 (not published)
- Files in alovefashion/theme (based on the NewMae kit), texts follow the Alove policy pages: free UK delivery,
  dispatch 1–2 business days, 7–11 business days total, 14-day returns + exchanges, refund within 10 business days,
  support@alovefashion.com. No policy, address, product or tracking changes.
- Look (different from Niaali): Playfair Display headings + Jost body (no bold body text), deep olive #2F3B2F header,
  buttons and footer, cream #F6F2EB announcement/trust/FAQ bands, pill buttons, trust icons in round circles,
  olive check circles, dot tier bar, muted red sale price/box. Footer: same business details, calmer layout.
- No "European" wording (UK audience).
- Product page: colour option shows the variant photo as swatch (snippets/variant-main-picker.liquid, settings
  show_variant_image + 44×55 swatches). Checkout texts in locales/en.default.json ("or pay securely below",
  free tracked UK delivery). About us page: "modern European style" sentence replaced (rest unchanged).

## Icons + square buttons (2026-10-12) – theme "Alove - iconen + vierkant (werk)" #202787815771 (copy of live kit, unpublished)
- Product benefits: olive check circles replaced by olive line icons (truck / return arrows / price tag), same 20px size,
  same 8px gap, rows stay 20px high on phone and desktop (blocks/pp-benefits.liquid: returns icon = same arrows as the cart;
  snippets/pp-alove-style.liquid: check-circle ::before removed).
- Square buttons store-wide: theme settings button_border_radius_primary/secondary 40→0, variant_button_radius 40→0,
  inputs_border_radius 4→0 (quantity selector, discount field), variant_swatch_radius 4→0; kit buttons .pp-chip, .pp-tab,
  .pp-card__quick, .pp-qp__add, .pp-row__arrow, .pp-home-cat__arrow → 0 (doubled class, the kit files load later).
- Kept round on purpose: trust icon circles, tier dots, badges, photo-slider dots, the X close icon, the quick-pick sheet corners.
- Product photos (same work theme, after GO): source photos are 1080×1080 squares, the gallery showed them portrait (1/1.25,
  cropped) at 2/3 of the width (895×1119 at 1440px → upscaled, blurry). templates/product.json: media-gallery aspect_ratio
  "1/1.25" → "1" (square, nothing cropped), main equal_columns false → true (50/50). Now 588px (1280), 668px (1440),
  708px (1920), full width on phones; no horizontal scroll.

## Rebrand to Migesi (www.migesi.com) – step 1, theme only (2026-10-14, after GO)
Live theme "Alove - iconen + vierkant (werk)" #202787815771 untouched (checksum verified). Work theme
"Migesi - rebrand (werk)" #202938876251 (copy of live, unpublished). Changed files in migesi-rebrand/theme:
- settings_data: logo Migesi_Logo_White.png (white copy of Elegant_Migesi_Serif_Wordmark.png, the header is dark
  green and the old Alove logo was white), favicon Migesi_Favicon_M.png (Elegant_Serif_Monogram_M.png padded to a
  square, 1536×1536, so the 32×32 crop does not cut the M). Logo heights unchanged (50 / 44).
- footer-group, index, product, page.contact: "ALOVE Fashion"/"Alove Fashion"/"ALOVE" → "Migesi",
  support@alovefashion.com → support@migesi.com, https://alovefashion.com/ → https://www.migesi.com/,
  Instagram link (alove__fashion) removed (user: "Haal link weg voor nu"). Business details (DK Interim Management,
  Venray address, KvK, VAT, phone) unchanged. CSS file name pp-alove-style left as is (not visible).
Still Alove in the preview (step 2+): store name (copyright, logo alt, titles), page bodies (FAQ, About, Terms,
Refund, Shipping, Payment, Contact Information), Shopify policies (Privacy, Contact information), vendor, SEO.
Noted: Payment page says prices are in Euros (EUR) while the store currency is GBP.
