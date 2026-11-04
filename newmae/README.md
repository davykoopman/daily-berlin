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
- Product: estimated delivery date available in blocks/pp-delivery (4–9 business days) but switched off at the owner's request (eta_min 0);
  mobile sticky add to cart shows the button text.
- Speed: gallery images after the first are lazy (snippets/product-media); pp-card variant JSON moved out of the page
  (fetched on "Choose" from /products/handle?view=pp-data → templates/product.pp-data.liquid + snippets/pp-card-data);
  quick pick JS in assets/pp-quick-pick.js (cached, once per page); desktop mega menu no longer preloads its images
  on phones (assets/header-menu.js); mobile hero max 960px.
- Measured (mobile, DPR 3, one run): product images 2060 → 1287 KB, home 1357 → 1110 KB, collection 1213 → 998 KB,
  HTML 40–75 KB smaller per page. Biggest remaining cost: Google tags loaded 4× (~680 KB JS), left to the owner.
- Look: text colour #1C1714 (warm black), announcement bar #1C1714, trust section as compact white cards with a warm border, no band behind (rust icon circle left, serif titles; 4 in a row on desktop, 2 x 2 on mobile), soft fade-in on scroll,
  slow zoom on product cards (desktop), square swatches on cards. Mobile hero cropped at 112% of the width (setting "Photo height mobile"), focal point bottom, so the models sit higher.
- Copied as is from the live theme (owner's decision): pp-rating "Rated by 2,000+ happy customers" and the
  customer photo section with invented names. FTC / Google Merchant Center risk; switch off before ads.
- Home proportions: trust cards, categories and bestsellers share one width (page width, 40px / 16px margins);
  categories and bestsellers both 5 per row on desktop (3 on tablet, 42vw on mobile), so tiles and product cards
  are the same size; on mobile the WOMEN/MEN switch sits under the title in both sections.

## Black Friday (2026-11-01, user GO: same as Davento/Niaali/Migesi, keep the 70% promotion and what is already there,
## Fall Clearance → Black Friday + bestsellers, 4 gifts, bundle discount off, rating + stock created but off)
Draft theme "Black Friday" #210137088325 = duplicate of live "Newmae - size guide (live) 29 Oct" #209889919301.
Files: black-friday/theme (changed/new), black-friday/orig (before), black-friday/data/bestsellers.json.
- LIVE STORE gifts ($19.95, type Gift, vendor Newmae, tags regalo + regalo-donna/-uomo, not tracked, no SKU, Online
  Store only, seo.hidden, in no collection, Davento photos): Marina Scarf (gift-marina-scarf), Card Holder
  (gift-card-holder), Classic Wallet (gift-classic-wallet), Curb Chain Bracelet (gift-curb-chain-bracelet).
- LIVE STORE discount "Free Gift" (gid://shopify/DiscountAutomaticNode/2266421035333): spend $90 on WOMEN or MEN,
  1 gift 100% off, once per order, combines with all, 1 Nov 00:00 UTC → 1 Dec 05:00 UTC (= 00:00 US Eastern).
  AOV last 365 days $62.49 (84 orders).
- Mix & Save 10/15/20% still ACTIVE on purpose (live theme advertises it). In the preview test Shopify applied
  Mix & Save 20% instead of the free gift (gift $19.95 in the cart) → deactivate the 3 Mix & Save discounts when the
  Black Friday theme is published (ids 2256740319557 / 2256740352325 / 2256740385093).
- LIVE STORE collections: Bestsellers Women (16) / Men (26) / Bestsellers (42, sub-collections) from sales in the
  last 120 days (summer items + drafts left out); Black Friday Sale (black-friday, compare-at > 0, 681),
  black-friday-women (463), black-friday-men (218) – same rules as fall-clearance (kept, not deleted).
  Main menu: "Bestsellers" after Home (backup black-friday/orig/main-menu.json).
- Theme:
  - Header: "BUY MORE, SAVE MORE" announcement off; sale banner = "BLACK FRIDAY · Up to 70% off | Free gift over $90 |
    Ends in …" (warm black #1c1714, countdown to 30 Nov 23:59 EST, links to /collections/black-friday).
    pp-gift-showcase in the header group with the gift bar OFF (setting show_bar; the banner says it) – loads palette,
    Cormorant 600 titles, rust "Bestsellers" menu pill, gift script.
  - Home hero: BLACK FRIDAY / Up to 70% off / "+ a free gift with orders over $90. Ends November 30." / Shop women's
    sale, Shop men's sale → black-friday-women / -men. "Black Friday Bestsellers" from bestsellers-women / -men.
  - snippets/pp-tier-progress shows the gift line while Black Friday runs (home bestsellers, collection head,
    product cross-sell); bundle bar back after 1 Dec. Cart totals: no bundle bar, saving without the gift's price.
  - Badge "BLACK FRIDAY" (warm black) on cards and the first product photo; chips All | Women | Men on the
    bestsellers and black-friday collections.
  - Product: third bullet "Free gift with orders over $90"; accordion Mix & Save → Free gift (pp-gift-tab);
    cross-sell title "Complete your order"; PP Rating OFF (prefilled 4.7 / 2,000+ as before), PP Stock OFF,
    delivery line OFF; sale badge stays off (end texts updated to November 30); photo directly under the banner on
    phones.
  - Cart: Black Friday sale line (warm black) + gift block on top (fast pick from Niaali/Migesi, standard
    shopify:cart:lines-update events), bin icon instead of "Remove", no quantity selector, "Free Gift" name hidden,
    add-ons "Complete your look · Black Friday bestsellers".
  - Not added: checkout line "Only 3% …" – not true for NewMae (5 of 84 orders refunded = 6%, $471.71 of $5,368 = 8.8%).
- Tested (preview, mobile 390 + desktop 1440): 12 pages, no Liquid/JS errors, no horizontal scroll, no Halloween /
  Fall Clearance / October 31 / Buy more / Mix & Save texts. Flow: $45.05 more under the minimum, pick in ~0.15 s,
  line in ~1.3 s, 3 rapid swaps → 1 gift, removing items below $90 removes the gift. Footer aligned (16px).
- Round 2 (user, 1 Nov): typographic Black Friday hero like the other stores (sections/pp-bf-hero: warm black,
  rust + champagne tapes, Cormorant title, offer in Manrope bold, "Up to 70% off", Women / Men → black-friday-women
  / -men, Shop bestsellers) first on the home page; photo hero (pp_hero) OFF, kept for after 1 Dec. Gift bar with the
  4 photos ON under the black banner (banner no longer repeats "Free gift over $90").
  Gift photos sharp: plain <img> with srcset 96w / 192w at 32px. Found: `image_tag: width: 32` also rewrites the
  file URL to width=32 (blurry) – the same code is in Davento v2, Niaali and Migesi pp-gift-showcase (fix there too).
- Round 3 (user, 1 Nov): black sale banner OFF (kept); "BLACK FRIDAY · UP TO 70% OFF" is now the first message in the
  announcement bar (links to /collections/black-friday), then free shipping and 60-day returns. Icons (trust row,
  gift bar, gift bullet, cart gift block) in the warm black #1c1714 on a soft warm grey circle instead of rust; rust
  stays for prices and -X% boxes (CSS in sections/pp-gift-showcase).
- Round 4 (user, 1 Nov): product photo without the "BLACK FRIDAY" label (only the variant photo; cards keep it).
  Everything Black Friday / discount in Black Friday red #c20000 (sale price, -X% box, pp cards, quick pick, cart
  add-ons, cart saving line, cart sale line, Black Friday label, Bestsellers menu tag, hero tapes + offer, gift bar
  and gift icons): --pp-red in pp-gift-showcase + overrides there. Primary buttons black (config/settings_data:
  palette_primary_button_background #65432B → foreground #1C1714). Trust cards stand out: warm grey card, black icon
  circle with a white icon, title 600.
- LIVE 1 Nov (owner published "Black Friday" #210137088325 = MAIN). Mix & Save 10/15/20% deactivated right after
  (EXPIRED, not deleted). Active automatic discount: only "Free Gift". Live test (no preview): $45.05 more under the
  minimum; over $90 pick → gift $0.00 in ~1 s, total $134.85 for 3 items (no Mix & Save any more), 3 rapid swaps →
  1 gift, removing items below $90 removes the gift; announcement "BLACK FRIDAY · UP TO 70% OFF", no Halloween /
  Fall Clearance text.
- The owner switched PP Rating ("4.7 · Rated by 2,000+ happy customers", manual) and PP Stock ON in the editor
  before publishing (templates/product.json 16:27, synced into black-friday/theme). 84 orders in the last 365 days,
  no review app → the 2,000+ claim is not backed by data (FTC rule on fake reviews / Google Merchant Center risk).

## Domain switch Newmae → Vinci (vincifashion.com), 4 Nov (agency checklist, user GO)
- Step 1 (ads off): done by the user. Domain www.vincifashion.com connected in Shopify (Namecheap DNS, SSL live),
  NOT primary yet.
- Step 2: theme copy "Vinci - domain switch (werk)" #210421350725 (duplicate of live "Black Friday" #210137088325).
  Logo VINCI_Elegant_Serif_Logo.png, favicon Vinci_Favicon_V.png (cleaned copy of Elegant_Black_Serif_V_Favicon.png:
  the upload had the grey "transparent" checker pattern baked into its pixels). Newmae → Vinci,
  support@newmae.com → support@vincifashion.com, newmae.com → vincifashion.com in config/settings_data,
  sections/footer-group, sections/pp-ugc, templates/index, product, collection, page.about-us, page.contact-us,
  page.faq (files in vinci/theme, originals in vinci/orig). Image file names (newmae-*.png) kept on purpose.
  Code comments "NewMae" left (not visible). Remaining "Newmae" on the site = store name (Settings → Store details:
  logo alt, hidden h1, copyright, schema.org) → changes when the owner renames the store.
- Step 3 prepared (vinci/texts/new, originals in texts/orig, ids in texts/ids.json): 5 Shopify policies
  (shopPolicyUpdate) and page payment-policy. Pages about-us / faqs / contact have no body (text is in the theme).
- Products: vendor "Newmae" on all 973 (incl. the 4 gifts), SEO title "… | Newmae" on 592; no "Newmae" in titles,
  descriptions or tags; collections and blog clean (old Fall Clearance collection texts still mention the bundle
  offer, unrelated to the switch). Data in vinci/data/p1–p4.json.
- Step B, 4 Nov (user GO), all checked:
  - Logo: the trimmed VINCI_Logo_Header.png (1457×321, no empty space) replaces the old logo, which had about 60%
    empty space. logo_height is 28 on desktop and 22 on mobile, so the logo shows noticeably bigger in the preview.
  - Page payment-policy: updated with pageUpdate.
  - Products: vendor is now "Vinci" on all 973 (0 still "Newmae"). The SEO title on 592 products changed from
    "| Newmae" to "| Vinci", with the existing SEO description sent along. Done with productUpdate in 13 batches
    (bulk operations and >16 KB documents are blocked in MCP, so the input goes in GraphQL variables).
    Afterwards all 973 were re-read: every SEO title is OK.
  - 5 Shopify policies: shopPolicyUpdate needs the scope write_legal_policies, which the MCP app does not have.
    The owner pastes texts/new/policy-*.html (Settings → Policies → <> HTML view).
  - Owner did step C: store name "Vinci Fashion", store email and sender email support@vincifashion.com
    (domain authenticated).
