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
- Round 5: top bar has the same thin divider between every part (headline | Buy more, save more | Ends in … →).
  Collection head tier bar back on (show_tiers true): "Add 2 more items and save 10%" → follows the cart.
- Round 6: "You save" line disabled (block kept, disabled). Mix & Save heading, tier text and bar centred
  (sections/pp-bundle.liquid + text_mix alignment). Product page order: main → trust icons → Mix & Save → customer
  photos → about → steps → FAQ. Note: customer photo section renders nothing because the image files were renamed
  in Files (CustomerPicture1–8) and the template still points to the old names.

## Cart and checkout (Fall Clearance theme copy, 2026-10-15)
- Drawer: pp-cart-saleline at the top (FALL CLEARANCE | Ends in …, hides after Oct 31) → items → pp-cart-upsell
  "Add 1 more & save X%" (pp-cards from fall-clearance-women/-men by cart gender, fallback fall-clearance, products
  in the cart left out, Choose opens pp-quick-pick, adds without leaving the cart). pp-quick-pick rendered once in
  snippets/cart-drawer.liquid so it works on every page.
- Cart page: same upsell row (8 products, 4 per row desktop) under the items (sections/main-cart.liquid).
- Under the total (snippets/tax-info.liquid): "You're saving $X on this order" = compare-at minus price per line +
  cart.total_discount (Mix & Save). Tier bar orange (#c2410c), texts: "10% off unlocked · add 1 more item to save 15%",
  max "You unlocked the maximum 20% off ✓".
- Quick pick sheet sale price and -X% box orange like the rest.
- Live store change: automatic discounts renamed "Mix & Save – 10/15/20% off" (rules unchanged: 2+/3+/4+).
- Tested in preview (desktop + mobile): add product → drawer shows sale line, upsell "save 10%", saving $44.95 →
  add shirt via upsell → 2 items, "save 15%", saving $104.39 (= 44.95 + 49.95 + 10% of 94.90), cart page the same.
- Hero fix: desktop height follows the photo (1960x802 → min(100vw*802/1960, 88svh)), photo anchored at the top;
  mobile 1.5× width (max 82svh), text at the bottom so faces stay free (CSS in sections/pp-home-best.liquid,
  scoped to hero_G7CAX9). Hero label "FALL CLEARANCE" without bold (h4 style), so the hero uses one serif heading
  and one sans font at one weight. templates/index.json built on the user's editor version (13:07).

## Speed & Premium (theme "Newmae - Speed & Premium (werk)" #208909107525, unpublished, copy of the live Fall Clearance theme)
- Files: newmae/speed/orig (as copied) and newmae/speed/theme (changed/new). No "Custom liquid" blocks were in use;
  everything is coded as sections/snippets.
- Quantity selector: product page only for products with quantity rules (hidden input quantity=1 otherwise,
  blocks/buy-buttons.liquid). Cart: selector only when a line has 2+, "Remove" text link (snippets/cart-products.liquid).
- Colour swatches without app/swatch data: colour options render square photo swatches (48px, 44px mobile) from the variant image,
  colour dot from the name as fallback (snippets/variant-main-picker, swatch, pp-color-hex). Swatch King app embed is
  still on in settings but renders nothing; if the app is reactivated, swatches would show twice.
- Cart upsell: compact rows (64px photo, title, price, "+ Add" → quick pick) in snippets/pp-cart-upsell.
- Home hero: own section sections/pp-hero (one <picture>, desktop/mobile photo, focal point settings, text left on
  desktop, bottom on mobile with a shade). Replaces the theme hero on index; old CSS hack removed from pp-home-best.
- Product: estimated delivery date (4–9 business days, US Eastern, computed in the browser) in blocks/pp-delivery;
  mobile sticky add to cart shows the button text.
- Speed: gallery images after the first are lazy (snippets/product-media); pp-card variant JSON moved out of the page
  (fetched on "Choose" from /products/handle?view=pp-data → templates/product.pp-data.liquid + snippets/pp-card-data);
  quick pick JS in assets/pp-quick-pick.js (cached, once per page); desktop mega menu no longer preloads its images
  on phones (assets/header-menu.js); mobile hero max 960px.
- Measured (mobile, DPR 3, one run): product images 2060 → 1287 KB, home 1357 → 1110 KB, collection 1213 → 998 KB,
  HTML 40–75 KB smaller per page. Biggest remaining cost: Google tags loaded 4× (~680 KB JS), left to the owner.
- Look: text colour #1C1714 (warm black), announcement bar #1C1714, cream trust band #F6F1EA, soft fade-in on scroll,
  slow zoom on product cards (desktop), square swatches on cards. Mobile hero cropped at 112% of the width (setting "Photo height mobile"), focal point bottom, so the models sit higher.
- Copied as is from the live theme (owner's decision): pp-rating "Rated by 2,000+ happy customers" and the
  customer photo section with invented names. FTC / Google Merchant Center risk; switch off before ads.
