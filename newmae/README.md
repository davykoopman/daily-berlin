# Newmae (newmae.com) – analysis before the kit

- Live theme: "Newmae" (Dwell 4.1.3 by Shopify, Horizon family – same block system as Niaali/Fabric) #203120181573
- Market: United States only, USD, English only. Free shipping (US), 60-day returns (customer pays
  return shipping), refund within 7 business days, support@newmae.com, reply within 12 working hours Mon–Fri.
- No active discounts (no bundle tiers yet).
- Menu: WOMEN / MEN (collection links with sub collections) – fits pp-collection-head, pp-home-categories, pp-home-best.
- Tracking in layout/theme.liquid: GA4 G-3JY106RSV4, Google Ads AW-18415220445.
- Baseline speed (mobile, 4x CPU): home LCP 1.2s TBT 0.9s 2.5MB; collection TBT 1.9s 3.4MB 397 req; product TBT 0.8s.
- theme-orig/: exact copies of the live files used for the analysis.

## Kit (theme "Newmae - kit (werk)" #207680405829, unpublished)
- Collection + search: pp-collection-head (title, tier bar, chips from main-menu), pp-card grid, pp-quick-pick
  (adds via /cart/add.js and fires the Dwell cart event, so the theme drawer opens and updates).
- Product: pp-title (h1) → price → pp-benefits (free shipping / 60-day money-back / buy more) → variants →
  add to cart → pp-delivery (1–2 days) → payment icons (enabled types) → accordion (details, shipping, returns,
  mix & save, linked to the policies) → Mix & save (pp-bundle) → pp-trust → About → pp-steps → pp-faq.
- Home: hero (Shop Women / Shop Men) → pp-trust → pp-home-categories → pp-home-best → About → pp-faq.
- Announcement bar: theme announcements, 3 messages, 4 s (free US shipping, tiers, 60-day returns).
- Footer: no business hours / GMT, "email us anytime". Trust card shows the support email instead of hours.
- Dwell differences vs Niaali/Fabric: no color schemes (color_palette), desktop scrolls inside .page-wrapper.
- Discounts (automatic, all products): Buy 2 save 10%, Buy 3 save 15%, Buy 4+ save 20%.
- Product page v2: gallery dots (no thumbnails), price 20px with red bold sale price + red -X% box
  (snippets/price.liquid), Swatch King swatches 44px (40px mobile), announcement bar 14px bold.
- Cart (drawer + page): tier progress bar + "Free shipping · 60-day returns · Secure checkout" under the
  total (snippets/tax-info.liquid), no currency code, prices in the body font (config/settings_data.json).
- Checkout texts (locales/en.default.json, shopify.checkout.*): free tracked shipping before the address,
  shipping line "Free", express divider "or pay securely below".

## Fall Clearance (theme "Newmae - Fall Clearance (werk)" #208681304389, unpublished, copy of the kit)
- Collections (smart, best selling, on Online Store): fall-clearance (compare-at > 0, 506 products),
  fall-clearance-women (+ type starts with Womens), fall-clearance-men (+ type starts with Mens).
- Sale ends 2026-10-31T23:59:59-04:00 (US Eastern). Banner, badge and countdown hide themselves after that.
  Prices and compare-at prices do not change by themselves: end the sale in the admin too.
- Colors: base #1A1A1A, accent burnt orange #C2410C (white text 5.2:1), #F97316 on black (7.5:1).
  Sale price and -X% box (snippets/price.liquid, snippets/pp-card.liquid) red → #C2410C.
- Announcement bar (4 s): FALL CLEARANCE · UP TO 50% OFF (orange) / BUY MORE, SAVE MORE · ENDS OCT 31 /
  FREE SHIPPING ON ALL US ORDERS / 60-DAY RETURNS.
- Home: hero with FALL CLEARANCE label, UP TO 50% OFF, orange buttons to the women/men sale collections →
  pp-sale-banner (countdown) → trust → categories → "Fall Clearance Bestsellers" (pp-home-best with
  sale_prefix fall-clearance-, sale_only) → about → FAQ.
- Collection: slim black pp-sale-banner with tiers and countdown above the head; tier bar in the head off.
- Product: pp-sale-badge (label + countdown, only on products with compare-at) → pp-rating (DISABLED) → title
  → price → benefits → variants → pp-stock (pulsing orange dot, "In stock, ready to ship", "Low in stock:
  only [n] left" only with real Shopify stock ≤ threshold 5, note "Popular styles sell out fast…") → buy buttons.
  Section pp-ugc "Styled by our customers" after the trust icons: hidden until it has a photo block.
- pp-rating: source "Review app" (reviews.rating / reviews.rating_count metafields) or "Manual" (4.7, "Rated
  by 2,000+ happy customers" prefilled at the user's request). Disabled in the template; only switch it on
  when the numbers are real (FTC review rule, GMC misrepresentation). Stock is ±99,999 per variant now, so
  the low stock line never shows until real stock is entered.
- Files: fall-clearance/theme (uploaded, md5 verified), fall-clearance/orig (before), screenshots/.
- Round 2 (user feedback): the sale banner now sits between the menu and the hero photo (home) and is written out in
  one colour (#C2410C background, white text, "FALL CLEARANCE · UP TO 50% OFF"). Hero label written out, no box.
  Product badge as orange text "FALL CLEARANCE · ENDS IN …". One orange everywhere (#F97316 removed, announcement
  text white). Hero height 100% → 80%. Product photo desktop: max 560px wide / fits the screen height
  (CSS in blocks/pp-title.liquid), equal columns. Colour options: screenshots/kleur-opties.png.
- Round 3: sale banner moved into the header group (every page), compact: "FALL CLEARANCE · UP TO 50% OFF" +
  small "Buy more, save more · Ends in 16d 15h 19m →", whole bar links to /collections/fall-clearance. Removed from
  the index and collection templates; the two sale messages left the announcement bar (shipping + returns stay).
  Product: sale badge is now a full-width orange bar. templates/product.json synced with the user's editor version
  (customer photo blocks added by the user).
- Round 4: product page sale bar replaced by "You save $X · Sale ends October 31" under the price (block pp-sale-badge,
  amount per selected variant = compare-at minus price). Top bar cleaner: more padding (11px), thin divider between
  headline and details on desktop, two lines on mobile; one section in the header group, so it changes on every page.
