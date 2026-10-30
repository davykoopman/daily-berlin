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
