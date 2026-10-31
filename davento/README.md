# Davento (davento.it) – Niaali kit on Apex

- Live theme: "Davento" (Apex 1.0.1, 200704459095) – untouched, rollback.
- Working copy: "Davento - kit (werk)" (206303068503), unpublished.
- `theme-apex-orig/` – exact copies of the Apex files before changes (md5 verified).
- `theme/` – kit files as uploaded to the working copy.

Store facts the kit follows (from the Davento policies, not Niaali):
IT primary + DE (`/de-de/`), EUR, free shipping, 60-day returns (customer pays
return shipping), support@davento.it, tiers 2:10 / 3:15 / 4:20.

Apex differences vs Horizon (Niaali):
- no `color_scheme` setting, no `spacing-style` / `gap-style` / `content_for`
- page wrapper `.amz-pw` (14px side padding on mobile), mobile ≤768px
- cart drawer opens on `ajaxProduct:added` dispatched from a form with `[name=id]`
- labels come from `pp-i18n`, not theme locale keys

## Steps
1. Collection page – done: `pp-collection-head` (title, tier bar, menu chips),
   `collection-grid` renders `pp-card` + `pp-quick-pick`.
2. Product page – done: `pp-benefits` (3 bullets), `pp-delivery`, `pp-payment-icons`
   (enabled checkout methods, one row), `pp-product-info` (accordion: details,
   shipping, returns, bundle), sections `pp-bundle`, `pp-trust`, `pp-steps`, `pp-faq`.
   Product page spacing: no Apex gaps, soft #f5f5f5 on "Chi siamo" and FAQ.
3. Homepage – done: hero (unchanged, translated) → `pp-trust` → `pp-home-categories`
   → `pp-home-best` (only the visible group in the page; the other loads in the
   background via `sections/pp-best-panel` + Section Rendering API) → Chi siamo → `pp-faq`.
   Old Donna/Uomo tiles and Apex FAQ kept in index.json but disabled (rollback).
   Other pages: search uses the pp-card grid (via collection-grid); cart line saving
   text was fixed English "Save" → IT "Risparmi" / DE "Du sparst" (snippets/cart-item).
4. Checkout texts – done (locales/it.json, locales/de.json; checkout uses them once the
   theme is published): express divider "oppure paga in modo sicuro qui sotto" /
   "oder unten sicher bezahlen", shipping placeholder "Spedizione gratuita con
   tracciamento…" / "Kostenloser Versand mit Sendungsverfolgung…", summary shipping
   line "Gratuita" / "Kostenlos", typo "Kostenlosser" fixed. Cart note "Prezzi IVA
   inclusa. Spedizione gratuita." / "Inkl. MwSt. Kostenloser Versand.", IT save
   text "Salva" → "Risparmi".
   Large files: upload via stagedUploadsCreate + themeFilesUpsert type URL (md5 checked).

## Shared header / product page extras
- `sections/pp-announcement.liquid` in `header-group.json` (Apex announcement kept, disabled):
  3 messages, IT/DE/EN from code, rotate every 4 s (pause only for a real mouse),
  one line down to 320 px wide.
- Product page desktop: photo column sticky under the header (Apex sets sticky but
  floats + `overflow-x: hidden` on #MainContent broke it; now flex + `overflow-x: clip`).
- `staged-upload.py`: helper for big theme files (stagedUploadsCreate → curl → themeFilesUpsert type URL).

## Switzerland / TWINT prep (2026-10-07, after GO)
Markets and domains are handled by the media buyer: CH market (CHF, /ch, German) and free shipping zone CH already exist.
Austria follows later, so country texts are written without a country list ("all countries selectable at checkout").
User wants own details in the background: legal notice only on /policies/legal-notice (Shopify links it in checkout),
no footer link. Customs/import costs left out of the texts on request.
- Footer menu: "Note legali" link added and removed again (menu back to the original 7 items).
- Page "Domande Frequenti": free shipping answer "…su ogni ordine in Italia e Germania…" → "…su ogni ordine…";
  "Spedite anche all'estero?" "Al momento effettuiamo consegne soltanto in Italia e Germania." →
  "Sì. Spediamo in tutti i paesi che puoi selezionare al momento del checkout."
- Page "Pagamenti": "in EUR (€)" → "in EUR (€) e, per gli ordini in Svizzera, in franchi svizzeri (CHF)". TWINT not listed
  until it is active.
- To paste by the user (no write_legal_policies): policies/legal_notice.it.txt / .de.txt and the shipping policy
  country paragraph in policies/shipping_country_paragraph.txt. Legal form: eenmanszaak (impresa individuale / Einzelunternehmen).
- Kit theme (unpublished by the user for these edits, live = old "Davento" theme meanwhile):
  `snippets/pp-payment-icons.liquid` and `sections/pp-faq.liquid` show/list TWINT only for visitors in CH
  (localization.country), FAQ names it "TWINT"; disabled Apex FAQ in index.json made country-neutral.
  The visible homepage FAQ (pp-faq) was already country-neutral.
- Full shipping policy to paste: policies/shipping_policy.it.html (German via T-Lab).

## Kleuren (2026-10-08) – theme "Davento - kleuren (werk)" #206722826583 (copy of live, unpublished)
Based on 10 dropship competitors (Drune, Harper & Wells, Karlson Berlin, Nordheim Mode, Moreau Lyon → Beaumont Nice,
Lumière Boutique, Laurent Monaco, Leon Boutique, Look de Paris, Wilson & Carter): white base, near-black text,
square buttons, one consistent accent; the high-volume ones use a green add-to-cart button.
Only config/settings_data.json changed:
- text, header text, announcement bar, footer, drawer text: #000/#0f0f0f → #1c1d1d (softer near-black)
- discount stays dark red #C20000 everywhere (A/B tested)
- custom CSS: add-to-cart + cart-drawer checkout button green #1f6b47 (hover #18563a); trust and benefit icons green;
  variant labels letter-spacing 0.04em; broken rule `.product__price.on-sale {color: #11b96f;` (no closing brace) replaced
  by `.product__price.on-sale{color:#c20000}` (the product page price keeps its own inline color from the price block)
- type_product_capitalize: true → false (product names in the grid no longer all caps)

## TWINT live (2026-10-09)
TWINT is active in the checkout (CH only, CHF). Checked on the live kit theme:
- Product page /de-ch/: 11 payment icons incl. TWINT; IT and /de-de/: 10 icons, no TWINT (pp-payment-icons, no change needed).
- Homepage FAQ (pp-faq) on /de-ch/ already names TWINT; not on IT/DE (no change needed).
- Policies: no policy lists payment methods (refunds go "to the payment method used", which covers TWINT) → no policy change.
Changed (pages, IT source text; German via T-Lab):
- "Pagamenti": list item "TWINT (solo per ordini in Svizzera)" after Klarna → pages/pagamenti.it.html
- "Domande Frequenti", payment answer: "…PayPal e Klarna. Per gli ordini in Svizzera puoi pagare anche con TWINT. …"
  (also removed the stray comma in "PayPal, e Klarna") → pages/faq-payment-answer.it.html

## Privacy policy restore (2026-10-14)
The user accidentally pasted the Migesi (Alove) privacy policy into Davento. Live check: default /policies/privacy-policy
showed "Migesi operates this store…"; the German translation (/de-de/, /de-ch/) still showed the Davento text.
Restore file policies/privacy_policy.it.restore.html = Shopify privacy template HTML with Davento values; text checked
word for word against the backup policies/privacy_policy.it.txt (2026-10-02): 2,725 words, 0 differences.
- Italian version policies/privacy_policy.it.italiano.html (same structure: 13 headings, 28 bullets, same 3 links and
  contact details; date 14 October 2026). The other Davento policies were already Italian; the privacy policy was the
  untranslated English Shopify template. The German translation (T-Lab) still holds the old Davento text.

## UK + FR translation prep (2026-10-28, after GO)
Locales en + fr added by the owner (unpublished); T-Lab AI translation running for both, all resource types except
shop policies. Markets UK/FR not created yet (media buyer). Policies are written by hand per country, not by T-Lab
(drafts, not in Shopify yet; register as en/fr translations of the shop policies after the owner approves):
- policies/en/*.en.html (UK): legal notice, contact (CET, "one hour ahead of UK time"), shipping, refund (60 days +
  Consumer Contracts Regulations 14-day cancel + Consumer Rights Act faulty items, refund ≤14 days after receipt),
  terms (statutory rights kept, liability per UK law, Dutch law + UK mandatory law and UK courts), privacy (Shopify
  template with Davento values, ICO line).
- policies/fr/*.fr.html (FR): mentions légales (directeur de la publication, hébergeur Shopify International Ltd Dublin,
  médiateur placeholder), contact (heure de Paris), livraison, retours (rétractation L221-18, garanties légales),
  CGV (official garantie légale de conformité text, vices cachés, Dutch law + French mandatory law, médiateur), privacy
  (CNIL line, directives post-mortem).
- Placeholders: [NOM DU MÉDIATEUR], [ADRESSE], [SITE INTERNET] in fr/legal_notice and fr/terms (art. 18).
- pages/en|fr/modulo-recesso.legal.*.html: replaces the "Diritto di recesso" part of page "Modulo di recesso" in the
  T-Lab translation (withdrawal possible before delivery too, statutory 14 days named, model cancellation form added).
  pages/en/pagamenti.currency.en.html: currency line with GBP for the "Pagamenti" translation.
- Same gaps exist in the IT/DE source (no model withdrawal form, "no withdrawal while in transit", Italian law, GMT+2
  all year) – advice to the owner, not changed.

## Black Friday Month (2026-10-30, user: theme "Black Friday" in draft, live Saturday 31 Oct evening)
- Theme "Black Friday" #208380952919 = duplicate of live "Davento - size guide (live) 29 Oct" #208314597719.
- Hero direction: option B (user's AI photo + Black Friday block as live, translatable text; desktop side by side,
  mobile photo on top). No text inside images (multi-market IT/DE/AT/CH/UK).
- Pricing check before "-50%": products mix compare-at (e.g. 42.95/85.90, 39.95/66.59) and no compare-at; tiers
  2/3/4 = 10/15/20% active. EU 30-day lowest-price rule applies to the announced reduction.
- Hero (user chose option 1, without free delivery / 60-day returns line): sections/pp-bf-hero.liquid in theme
  "Black Friday" (black-friday/theme/). Texts in code per language (it, de, fr, else English), "up to"/flat switch in
  the section settings, Anton font via font_picker, buttons to collections donna/uomo (localized URLs).
  templates/index.json: pp_bf_hero first, Halloween slideshow disabled (kept for rollback; original in black-friday/orig/).
  Preview checked IT, /de-de, /en-gb on mobile + desktop. Page errors "$ is not defined" and "reading 'dataset'"
  also on the live theme (not from the hero). FR has no market yet, so not previewable.
- Categories + bestsellers + collection page made identical (user: same image sizes, arrows, look):
  sections/pp-home-categories.liquid now uses the shared pp-row (same track, 4 columns, 12px gap, overlay arrows,
  pp-bundle__all "see all" tile) and pp-quick-pick for the arrows (own script and row/nav CSS removed).
  snippets/pp-card.liquid: arrows centred on the first photo (container query), mobile row edge 14px (= .amz-pw),
  collection/search grid gap 12px desktop / 10px mobile, theme's 3px mobile offset on the collection column removed.
  Measured in preview: desktop cat/best/collection/product-page row 341×426, gap 12, arrow on photo centre;
  mobile rows 164×205 at 14px, collection 2 per row at 14px, gap 10. Tablet (750–989): rows 3, collection grid 4 (theme).
  Originals in black-friday/orig/.
- Hero font Anton → DM Serif Display (user: more classic, same design with tapes). Font variable moved into the
  {% style %} block (family names with quotes broke the inline style attribute). Checked IT, /de-de, /en-gb mobile + desktop.
  Seen on /en-gb: main menu says "Woman" / "Man" (should be Women / Men) – menu translation, not changed yet.
- Red Black Friday corner ribbon (user chose A, in red, not too big): snippets/pp-bf-ribbon.liquid, rendered in
  pp-card (all cards: home bestsellers, collections, search, product page row) with "BLACK FRIDAY" and on the product
  page photo (snippets/product-images.liquid, inside .product__main-photos) with the product's own discount
  ("BLACK FRIDAY · -50%"; only "BLACK FRIDAY" when there is no compare-at price). Sizes: card 96px corner (72px mobile),
  product page 180px (140px mobile). Hides itself from 1 Dec 2026 00:00 Italian time (bf_end in the snippet).
  Not on the image files, so the Google Shopping images stay clean. Category tiles have no ribbon.
- Trust bar option C everywhere pp-trust is used (home + product page): sections/pp-trust.liquid shows a red tape that
  slowly scrolls (60s loop, pauses on hover, still for reduced motion) with "BLACK FRIDAY · <offer> · <free shipping> ·
  <returns> · <secure payments>" in the visitor's language, plus a compact icon + title row (subtitles hidden).
  Offer text setting "bf_offer" (upto/flat) in the section. snippets/pp-bf-active.liquid holds the one end date
  (1 Dec 2026 00:00 Italian time) for ribbon and tape; afterwards the normal trust bar returns by itself.
  Checked IT, /de-de, /en-gb on mobile + desktop, home and product page.
- Trust bar changed to option B look (user: no moving tape, "too busy"; size/layout of the compact row, a bit more
  spread out; own section apart from the hero): cream #f3efe8 band, red icons, titles in DM Serif Display (font picker
  "bf_font" in the section), thin #ddd5c9 separators, 1320px wide row; mobile 2×2 with left-aligned titles. Tape markup,
  CSS and the "bf_offer" setting removed. Hero bottom ribbons lifted (desktop 64/84px, mobile 22px) so a dark strip
  separates the hero from the cream band. Still only until 1 Dec (pp-bf-active), then the normal trust bar.
  Seen: /de-de menu tabs say "Frau / Mann" (should be Damen / Herren), /en-gb "Woman / Man" – menu translations.
- Uploaded after the user's "Doe opnieuw" (first upload was denied) and checked in preview IT + /en-gb, mobile + desktop:
  hero cream ribbons mirror the red ones (same length, leave the hero at the bottom edge); trust bar during Black
  Friday = own white section with four equal cream cards (14px radius, 16px gap desktop / 10px mobile, 2×2),
  cards rise in on load one after the other and each icon pops once (no scroll reveal; still for reduced motion).
- Colours: 4-colour palette (user: max 3–4 colours, buttons black). One place: the :root block in snippets/pp-card.liquid
  (--pp-ink #1c1d1d, --pp-white, --pp-cream #f3efe8, --pp-red #c20000; also maps --color-foreground(-rgb/-heading),
  --color-background that the pp files use). All pp sections/snippets point to these: #030302 / #000 / #111 / #141414
  → ink, rgb(3 3 2 / .76) → ink 70%, #f5f5f5 / #f3f3f3 / grey image placeholders / "see all" tiles → cream,
  rgb(194 0 0) / #c20000 → red, black borders → ink 12%; hero = one ink with a soft light centre, kicker/sub in cream.
  Theme settings (config/settings_data.json): body/header/drawer/footer text, announcement, large image bg, footer,
  drawer button, compare/current price → #1c1d1d; borders → #e4e4e4; sale colours #c20000; broken custom CSS
  ".product__price.on-sale {color: #11b96f;" → ".product__price.on-sale{color:#c20000}".
  templates/product.json price block: sale price red #c20000 (like the cards), compare and regular price ink.
  Checked in preview (home, collection, product page): only ink, white, cream, red (+ ink transparencies) remain;
  Apex's selected size button (#292929) is theme CSS and left as is. Originals in black-friday/orig/.
- NewMae-style blocks, all OFF in templates/product.json (switch on per block in the theme editor):
  pp_rating (snippets/pp-rating.liquid, first block): stars + "4.7/5 · Valutato da oltre 2.000 clienti soddisfatti"
  per language. source 'app' reads the reviews.rating / rating_count metafields (none exist now, so it shows
  nothing); source 'manual' uses manual_rating / manual_count – only with real numbers (no fake social proof).
  pp_stock (snippets/pp-stock.liquid, above buy buttons): pulsing dot + "Disponibile, pronto per la spedizione"
  + note; low-stock text only from real Shopify stock ≤ threshold 5; follows the variant. Tested with a temporary
  template templates/product.pp-test.json (IT desktop, DE + EN mobile). The API may not delete theme files:
  delete that template in the admin (Edit code) – it is only reachable with ?view=pp-test.
- Cart drawer (snippets/cart-drawer.liquid, Apex original in orig/): "Completa il tuo look" add-on row
  (snippets/pp-cart-upsell.liquid: donna/uomo pool picked from the cart, hides products already in the cart,
  + opens the quick pick) and 3 perks under it (snippets/pp-cart-perks.liquid: free shipping · 60-day returns ·
  secure checkout). JSON for the quick pick moved to snippets/pp-card-data.liquid.
- Checkout text "oppure paga in modo sicuro qui sotto" (shopify.checkout.alternative_payment_method_banner.or)
  → "Solo il 3% ha usato la nostra garanzia soddisfatti o rimborsati" (it/de/en/fr locales). 3% not 2%: refunds
  are 54 of 1,940 orders = 2.8%. Applies once this theme is published.
- Product page tighter: thumbnails hidden, the theme's slider dots shown on the photo (desktop + mobile) with
  hover arrows on desktop (snippets/pp-gallery-nav.liquid, rendered in product-images.liquid); "Spedito entro
  1–2 giorni lavorativi" block (pp_delivery) disabled; block spacing 25px → 16px (title 10px), variant label
  spacing smaller. pp-rating: no "+" after "oltre / über / plus de".
- Rating and stock rebuilt as own block types (user: on/off exactly like NewMae): "PP Rating" and "PP Stock" in
  sections/main-product.liquid (rendered in snippets/product-template.liquid; Apex originals in orig/). Both in
  templates/product.json, disabled; switch on/off with the eye in the theme editor, settings per block.
  PP Rating: always above the title (wherever the block is in the list), source Manual (default: 4.7, 2000
  customers, translated text; optional own text) or Review app; one line on phones (DE text "Über 2.000
  zufriedene Kunden"). PP Stock: no stock rule any more (user: "risico op mij") – dot + "Disponibile, pronto per
  la spedizione" + note on every product while on, hidden only on a sold-out variant; own line/note text optional.
  Tested on/off with templates/product.pp-test.json (IT/DE/EN, mobile + desktop).
- PP Stock: note under the line off (user), setting "Show note" default off; only dot + "Disponibile, pronto per la spedizione".
- Product page ribbon: only "BLACK FRIDAY" (user: the percentage is already next to the price); a bit smaller
  now the text is shorter (150px desktop / 120px mobile).
- Hero kicker without the shop name ("TUTTO NOVEMBRE"). Sparkle options A (gold foil edges + shine + gold title),
  B (glitter tapes + twinkles), C (gold dust + glow) shown as preview screenshots only; waiting for the user's pick.
- Hero (user picked V3 without the bronze frame on the offer): bottom ribbons bronze-gold gradient, kicker bronze
  #d6a874, title white, offer red. Satin shine (white streak) runs over the 4 ribbons and the offer one after the
  other every 7s (CSS only, off for reduced motion). Only in sections/pp-bf-hero.liquid; rest of the site keeps
  ink/white/cream/red. Checked IT + /de-de, mobile + desktop.
- Hero entrance animation (once on load, CSS only): kicker and title visible from the first frame and settle
  (opacity .3/.35 → 1, 16px rise; never invisible, so LCP is not delayed), offer stamps in at 0.5s (scale 1.9,
  -12° → -3°), sub + buttons fade up at 0.85/0.95s. Off for reduced motion. Checked mobile + desktop, end state ok.
- No quantity selector anywhere (owner: nobody uses it): hidden in snippets/cart-item.liquid (drawer + /cart page;
  the input stays for the theme's cart form), small "Rimuovi"/remove link shown instead. In the drawer the link uses
  the theme's hidden minus button so the drawer updates in place (snippets/pp-cart-perks.liquid script). Product page
  and quick pick had no quantity field. Cart perks smaller (11px text, 13px icons). Tested mobile + desktop.
- Cart "Completa il tuo look" simplified (user: less text): photo tiles (4:5) with a round black "+" on the photo and
  only the price under it; no names, no "Aggiungi" text. 3 per row on desktop, 2.6 on mobile (third tile peeks, so it
  is clear the row swipes). Adding from a tile tested IT desktop + EN mobile (cart 1 → 2).
- Automatic discounts renamed in the live store (user asked): "2/3/4 articoli = 10/15/20% di sconto" →
  "Mix & Save -10%", "-15%", "-20%" (still active, same rules). Discount titles are not translatable in Shopify
  (no discount type in TranslatableResourceType / Translate & Adapt), so one neutral name works for all markets.
- Home categories + bestsellers: 5 per row on desktop (was 4; index.json pp-home-best columns 5, pp-home-categories
  --pp-row-columns 5). Category photos (new Christmas shots are portrait 2:3) now show in full at 2:3, so no cut
  heads or heels; "see all" tile 2:3 too; category arrows centred on the 2:3 photo. Bestsellers stay 4:5.
  Tablet 3 per row and mobile swipe width unchanged. New category photos should be shot 2:3.
- Analysis 31 Oct (advice only, nothing changed): speed (mobile, slow 4G + 4x CPU, draft): product LCP 1.8s, home
  hero title 1.7s; the late "LCP" (4–5s) is Shopify's cookie banner text. 175 requests, ~1.4 MB; images ~0.7 MB;
  22 below-the-fold images load eagerly on collections (8 on home). Scripts: pixels (wpm 83 KB, Klaviyo, Clarity,
  wetracked, Google Ads) – tracking, not touched. Traffic 30d: 88% mobile; mobile ATC 5.1%, checkout reached 65% of
  ATC, conversion 1.44%. Top sellers mostly -50% (-40% some); 3 top sellers are DRAFT (cargo uomo, completo uomo
  occasioni speciali, completo donna eleganti). Mockups: dark header + red "Black Friday -50%" menu pill + bronze
  hero link + minimal trust row (recommended), cream header + dark trust cards (alternative), new home titles.
- 31 Oct, "werk het allemaal uit" (all in draft #208380952919 unless noted):
  - Home titles: "Shop per categoria" / "I più venduti" (translated per language, no red kicker), in DM Serif
    Display, sentence case, 34px (26px mobile) – snippets/pp-gender-tabs.liquid + the two home sections.
  - Trust row during Black Friday: no cream boxes; one white row, fine ink icons, small uppercase titles, thin
    dividers (2x2 on phones); the unused serif font is no longer loaded (sections/pp-trust.liquid).
  - Hero: small bronze link "Scopri i bestseller Black Friday →" under the buttons (setting collection_best =
    black-friday in index.json; texts IT/DE/FR/EN).
  - Product page: sticky add-to-cart on (enable_sticky_atc, mobile + desktop).
  - Cart drawer: tier bar ("Aggiungi ancora 1 prodotto e risparmia il 10%") on cream at the top; refreshes on
    drawerOpen too.
  - Header: tried a dark header – user did not like the colours, so back to the white header. Only the menu link
    to /collections/black-friday is a red pill while the sale runs (snippets/pp-bf-header.liquid, rendered from
    sections/pp-announcement.liquid, which also got French texts). assets/pp-logo-white.png from the dark try is
    unused (the API may not delete theme files).
  - LIVE STORE: collections "Black Friday Bestsellers" (black-friday, 17 products), "… Donna" (9) and "… Uomo" (9),
    manual order by sales of the last 60 days, published like donna/uomo, titles/descriptions translated DE/EN/FR.
    Main menu: item "Black Friday" after Home (no sub items, so the home gender tabs stay Donna/Uomo).
    Backup of the menu before: black-friday/orig/main-menu.json.
  - Images below the fold: checked – they already have no src until needed, nothing to change.
  - Editor changes in product.json/index.json (Christmas image in "Chi siamo", bf_font) were merged, not overwritten.
- Free gift (LIVE STORE, 31 Oct): 4 products listed for the "free gift above €80" plan, price €19,95 each, tag
  regalo + regalo-donna / regalo-uomo, type Regalo, inventory not tracked, active + published (needed to add them
  to the cart), hidden from search (seo.hidden = 1), in no collection; titles/descriptions translated (EN text
  without the € amount because of the GBP market):
  Foulard Marina (/products/regalo-foulard-marina), Portacarte Nero (regalo-portacarte-nero) – women;
  Portafoglio Classico (regalo-portafoglio-classico), Bracciale Grumetta (regalo-bracciale-grumetta) – men.
  Not built yet (waiting for GO): automatic "Regalo gratuito" discount (buy X get Y, €80 on non-gift products,
  1 gift at 100%), Mix & Save excluding gifts, gift picker + €80 progress in the cart drawer.
- Free gift replaces Mix & Save (user GO, 31 Oct):
  - LIVE STORE: Mix & Save -10/-15/-20% deactivated (status expired, not deleted – reactivate in Discounts).
    New automatic discount "Free Gift" (gid://shopify/DiscountAutomaticNode/1956016816471): buy at least €80 from
    the collections Donna or Uomo (gifts are in neither), get 1 of the 4 regalo products 100% off, once per order,
    combines with product/order/shipping discounts. Title is not translatable (Shopify), so it is in English.
  - Theme (draft): snippets/pp-gift-min (the 4 gift handles + minimum €80 in one place; converts the amount to
    the visitor's currency), pp-gift-text (all gift texts IT/DE/FR/EN), pp-gift-cart (cart drawer block: progress
    "Ancora €X…", gifts locked under €80, pick/swap from €80, gift removed automatically under €80, max 1;
    layout 'line' = progress line on pages), sections/pp-gift-showcase (home: cream band with the 4 gifts, after
    the trust row). Replaced the bundle discount everywhere: announcement (gift message first), product page
    bullet (pp-benefits, original in orig/), product info tab "Regalo gratuito", product cross-sell title
    "Completa il tuo ordine" + gift line, collection head and home bestsellers (gift line instead of tier bar),
    cart drawer (gift block instead of tier bar). pp-tier-progress is no longer used.
  - Tested (preview, mobile + desktop): announcement + product bullet + product tab + cross-sell + home section show
    the gift; cart under €80 "Ancora €45,05…" with locked gifts; from €80 pick → gift line €0,00 (discount applied),
    swap works, removing an item under €80 removes the gift; checkout €117,85 → €97,90 with the gift free.
    UK shows "£68" / "£67.98 more" (converted), DE in German. Amounts use the store money format (€45,05).
    Note: Shopify's bot check blocks a headless browser now and then; tests use a normal browser identity.
- Gift strip instead of the big home section (user: "veel kleiner", idea: under the menu on every page): section
  pp-gift-showcase is now a slim cream bar (45px desktop / 41px mobile): gift icon + "Regalo gratuito per ordini
  sopra €80" + the 4 gifts as 32px (26px mobile) photos. Placed in sections/header-group.json after the header
  (every page; original in orig/sections/header-group.json), removed from index.json. The announcement bar no longer
  repeats the gift (rotates free shipping / 60-day returns). Checked home + collection, desktop + mobile.
- Product page gift line is personal (snippets/pp-benefits.liquid): this product (current variant) + the cart against
  the €80 minimum → "Con questo articolo ricevi un regalo gratuito ✓" or "Con questo articolo mancano solo €45,05 per
  un regalo gratuito" (DE/FR/EN too, UK in £); follows variant and cart changes; general text if the script fails.
- LIVE STORE: "Black Friday" renamed "Bestseller" (user: Black Friday sounds odd as a collection): menu item
  (EN Bestsellers, DE Bestseller, FR Best-sellers) and the collections Bestseller / Bestseller Donna / Bestseller Uomo
  (DE … Damen/Herren, EN Bestsellers Women/Men, FR Best-sellers Femme/Homme). Handles stay black-friday(-donna/-uomo),
  so links and the red menu pill keep working.
- Mobile product page alignment (user: not aligned): the theme gave the product column 3px extra left padding on
  phones (17 vs 14px everywhere else) → removed, photo full-bleed with -14px (now exactly 0..screen width, no
  sideways scroll). Sizes on one line on phones (button pickers only, equal width). Cross-sell title "Completa il
  tuo ordine" in DM Serif like the home titles (pp-trust loads the bf_font again for that). Benefit bullets
  top-aligned and the gift line shortened to one line ("Ancora €7,05 per un regalo gratuito" / "Regalo gratuito
  incluso ✓", DE/FR/EN too). Gift strip on phones uses a short text ("Regalo gratuito sopra €80") so it stays on one
  line. Checked at 375 and 390px.
- All titles in DM Serif Display, sentence case (user): sections/pp-gift-showcase (header group, every page) has a
  font picker "Title font (all pages)" (default dm_serif_display_n4), loads it and sets h1/h2/.h1/.h2, product title,
  collection title, home/cross-sell titles to it (no uppercase, no letter spacing). Theme setting
  type_header_font_family (Tenor Sans) left untouched. Footer headings follow too.
  Collection page: gift line centred under the centred title. Hero link shortened to "Scopri i bestseller →"
  (DE Bestseller entdecken, FR Voir les best-sellers, EN Shop bestsellers). Checked collection, product, home,
  mobile 390 + desktop 1440.
- Bestseller collections much bigger (LIVE STORE, user): every product that sold ≥2 units in the last 120 days
  (list in black-friday/data/bestsellers-120d.txt, bathrobe and bra left out) → Bestseller Donna 123, Bestseller
  Uomo 126 (split by donna/uomo/unisex in the title), sorted Best selling. "Bestseller" (black-friday) now uses
  both as sub-collections (248, stays in sync). Drafts in the list do not show in the shop.
  Theme: Bestseller pages get chips Tutto | Donna | Uomo (DE Alle/Damen/Herren, FR Tout/Femme/Homme, EN All/Women/
  Men) in pp-collection-head; chips are centred on phones when they fit, otherwise swipe from the left as before.
- Fix: the free gift strip lost its cream background and red icon on pages without product cards (contact, FAQ,
  about). The palette (--pp-*) was only defined in snippets/pp-card. It is now also in pp-gift-showcase (header
  group, every page), so the strip and the cart drawer look the same everywhere.
