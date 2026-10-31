# Niaali – productpagina (Fabric-thema)

Herbruikbare productpagina-opzet ("PP-kit") voor alle stores. Gebouwd en getest op Niaali
(thema-kopie "Fabric - Product page v2", nog niet gepubliceerd).

## Bestanden
| Bestand | Wat het doet |
|---|---|
| `theme/blocks/pp-title.liquid` | Producttitel als `<h1>`, 20px mobiel → 24px desktop |
| `theme/blocks/pp-benefits.liquid` | 3 bullets met icoon: gratis verzending, X-dagen geld-terug-garantie (link naar refund policy), buy more save more. Instelling *Return period in days* per store gelijkzetten aan de refund policy |
| `theme/snippets/pp-i18n.liquid` | Vertalingen voor de kit op basis van de taal van de bezoeker (pl, en, nl, de, fr, it, es; anders Engels) |
| `theme/snippets/price1.liquid` | Prijs: kortingsprijs vet en rood, normale prijs zwart, rood -X%-vakje uit de compare-at-prijs |
| `theme/snippets/cart-products.liquid` | Winkelwagen: kortingsprijs vet en rood (klasse `pp-sale-price`, CSS in `pp-benefits`) |
| `theme/snippets/pp-tier-progress.liquid` | Staffel-voortgangsbalk in Mix & match: leest het aantal producten in de winkelwagen en toont live "Dodaj jeszcze 1 produkt i oszczędź 10%" met een dunne balk in 3 stappen, zonder labels (eerlijke urgency). Instelling `2:10,3:15,4:20` gelijk aan de kortings-app |
| `theme/snippets/pp-tiers.liquid` | (Niet meer in gebruik) staffel als labels |
| `theme/snippets/pp-reveal.liquid` | Rustig verschijnen bij scrollen (iconenrij en stappen), uit bij "minder beweging" |
| `theme/sections/pp-bundle.liquid` | Mix & match: producten uit dezelfde menugroep als het product (Kobiety/Mężczyźni, uit het hoofdmenu), staffel-voortgangsbalk onder de kop, tegel "Bekijk hele collectie", kaart-hover op desktop |
| `theme/blocks/pp-delivery.liquid` | Levertijd onder de knop: "Verzonden binnen [x] werkdagen". Dagen per store gelijkzetten aan de verzendpolicy |
| `theme/sections/header-group.json` | Aankondigingsbalk: 3 wisselende berichten (gratis verzending, staffelkorting, retourdagen), om de 4 sec, op mobiel 1 regel. Teksten per store aanpassen aan de echte staffel en policy, vertalen via *Translate & Adapt* |
| `theme/sections/pp-trust.liquid` | Iconenrij met 4 garanties (verzending, retour + ruilen, veilig betalen, klantenservice met echte openingstijden, klikbaar naar e-mail). Instellingen: retourdagen, e-mail (leeg = store-e-mail), openingstijden en tijdzone (wordt in andere talen dan de hoofdtaal getoond, bv. "(CET)" op /gb). Teksten kort gehouden zodat alles op 1 regel past |
| `theme/sections/pp-steps.liquid` | "Zo werkt het" in 3 stappen (bestellen, thuis passen, niet goed = retour/ruilen). Instellingen: verzenddagen en retourdagen |
| `theme/sections/pp-collection-head.liquid` | Collectiepagina: compacte titel, staffel-voortgangsbalk en categorieknoppen uit het hoofdmenu (de subitems van de groep waar de collectie onder valt, met de menutitels, actieve knop zwart, op mobiel swipebaar). Bevat ook de CSS voor het productgrid: 4 kolommen desktop / 2 mobiel binnen paginabreedte, geen "W PROMOCJI"-labels, titel/prijs/kleuren altijd op 1 regel |
| `theme/sections/pp-home-categories.liquid` | Homepage: subcollecties uit het hoofdmenu als fototegels met een Kobiety/Mężczyźni-schakelaar (labels = menutitels, volgorde = menuvolgorde), één swipebare rij (6 per rij op desktop), laatste tegel linkt naar de hoofdcollectie. Foto = collectieafbeelding, of de eerste productfoto als de collectie er geen heeft |
| `theme/sections/pp-home-best.liquid` | Homepage: bestsellers (volgorde van de collectie, staat op Best verkocht) met dezelfde Kobiety/Mężczyźni-schakelaar, staffel-voortgangsbalk en dezelfde kaartjes als "Łącz i oszczędzaj" |
| `theme/snippets/pp-gender-tabs.liquid` | Groepsschakelaar voor de homepage: elke collectielink in het hoofdmenu met subitems wordt een knop. De keuze geldt voor alle secties op de pagina en wordt per bezoek onthouden |
| `theme/snippets/pp-card.liquid` | Licht productkaartje voor alle productlijsten (homepage-bestsellers, Mix & match, collectie- en zoekpagina): 1 foto (2e foto bij hover, pas geladen als de muis erop staat), kleurfoto's direct in het thema (geen app), titel/prijs/-X% op 1 regel, knop "Wybierz" altijd zichtbaar. ±7 KB per kaartje i.p.v. ±28 KB. Bevat ook de CSS van de scrollrij (swipen op mobiel, pijlen op desktop) |
| `theme/sections/main-collection.liquid`, `theme/sections/search-results.liquid` | Collectie- en zoekpagina gebruiken ook `pp-card` + `pp-quick-pick` (alleen de kaartregel is vervangen; filters, sorteren en pagina's zijn van het thema). Collectiepagina 1,42 MB → 0,94 MB |
| `theme/snippets/pp-quick-pick.liquid` | Eigen keuzevenster (kleur + maat) voor pp-card: opent direct zonder laden (productgegevens staan klein in de pagina), voegt toe via /cart/add.js waarna de Kaching-winkelwagen zelf opent (zonder winkelwagen-app: naar de winkelwagenpagina). Teksten uit de themavertalingen, dus elke taal |
| `theme/assets/quick-add.js` | Snel toevoegen (knopje op productkaarten): laadt alleen de productsectie in plaats van de hele productpagina (±145 KB i.p.v. ±900 KB; de sectie-id wordt per bezoek geleerd, dus werkt op elke store), begint al te laden bij hover (desktop) of aanraken (mobiel), deelt geladen producten tussen secties, knop pulseert tijdens laden, en gaat naar de productpagina als laden mislukt |
| `theme/snippets/quick-add-modal.liquid` | Snel-toevoegen-venster: de kleur/maat-kiezer van Swatch King wordt nu ook op desktop getoond (het thema verborg alles wat het niet kende) |
| `theme/snippets/pp-see-all-key.liquid` | Kiest de tekst van de tegel "Bekijk hele collectie" (dames/heren/neutraal) op basis van de groepscollectie, in elke taal |
| `theme/templates/index.json` | Homepage: banner → trust-punten → categorieën → bestsellers → O nas → FAQ (FAQ in lijn met de policies) |
| `theme/templates/collection.json` | Collectie-template: PP Collection heading + productgrid (kaarten zonder inspringing, 4:5 foto's) |
| `theme/templates/product.json` | Volgorde: titel → prijs → bullets → kleuren → maten → zwarte Add to cart → betaaliconen (automatisch, wat actief is) |
| `*.original.*` | Back-up van de bestanden vóór de wijziging |

Mix & match (`pp-bundle`): kop + staffel-voortgangsbalk, 4 kaarten desktop / 2 + swipen mobiel, -X% vakje, "W PROMOCJI"-label verborgen, titels max 2 regels, quick add ook op mobiel (CSS in `pp-benefits`, inclusief fix voor de Swatch King-kiezer in het quick add-venster). Volgorde: productinfo → Mix & match → iconenrij → O nas → Zo werkt het → FAQ. O nas op mobiel: lagere foto, tekst links.

Menu = enige bron: groepen en categorieën komen uit het hoofdmenu (`main-menu`, per sectie te wijzigen). Een collectielink op het hoogste niveau met subitems is een groep (Kobiety, Mężczyźni); de collectie-subitems zijn de categorieën. Nieuwe categorie = collectie aanmaken en als subitem onder de groep in het menu zetten; homepage, collectieknoppen, bestsellers en Mix & match volgen vanzelf. Lege collecties en een subitem dat naar de groep zelf linkt ("Zobacz wszystko") worden overgeslagen. Vertalingen (T-Lab) vertalen alleen de menutitels, de links blijven kloppen.

Foto's: carousel in 4:5 staand kader, begrensd op schermhoogte, bolletjes op mobiel en desktop.

## Op een nieuwe store zetten
1. Thema dupliceren, bovenstaande bestanden uploaden in de kopie.
2. In de template `return_days` gelijkzetten aan de refund policy van die store; staffel invullen. Hoofdmenu opbouwen als groep → subcollecties (zie boven); verder geen handles nodig.
   In *Theme settings* "Currency code" op productpagina's uit.
3. Teksten in de template (accordions/FAQ) in de hoofdtaal zetten en via *Translate & Adapt* vertalen.
4. Controleren in preview, per markt, op mobiel en desktop. Daarna pas publiceren.

## Policies
`policies/` bevat de verzendpolicy (Pools en Engels) met algemene landen-zin en gratis verzending, plus back-ups (`*.original.*`).

## Drafted 20 summer products (2026-10-12, after GO)
Active products with an SS/summer tag and 0 sales since 2025-01-01 (all added Sep–Oct 2026). Active 639 → 619.
Reactivate in spring. IDs (gid://shopify/Product/…):
16091118534988 sandały na obcasie letnie · 16091822948684 sandały z paskiem · 16148222738764 klapki japonki ·
16124809969996 chodaki letnie · 16091823112524 sukienka midi na lato · 16148241023308 letnie spodnie szerokie ·
16145868816716 szerokie spodnie z gumką · 16126307828044 długa spódnica · 16129830158668 sweter na lato ·
16169668018508 komplet sukienka w kwiaty + kardigan · 16080385147212 komplet bluzka + spodnie ·
16091096809804 półbuty wiosenne · 16091096908108 sneakersy wiosenne · 16091823243596 mokasyny z klamrą ·
16179474170188 polo golfista · 16080381018444 zestaw koszulka + szorty · 16145829790028 komplet sportowy szorty ·
16148217856332 czapka z siateczki · 16132408672588 koszula wielobarwna · 16143363670348 garnitur na letnie uroczystości
Kept active: the 13 summer-tagged products with sales (e.g. eleganckie mokasyny 33×, sukienka koronkowa 13×) and
year-round items (trousers, suits, pumps, sneakers, long-sleeve shirts, pyjamas, party sets).

## NL market review (2026-10-18)
NL market: niaali.com/nl-nl/, language nl, EUR. Reviewed home, all menu collections, products, filters, quick pick,
search, cart (drawer + page), all pages and policies, 404, order tracking and checkout, on mobile and desktop.
- OK in Dutch: theme texts, menus, filters, product titles/descriptions (961 of 962 translated; the one left is archived),
  collections, pages, policies, SEO title/description, checkout.
- Fixed live (pages/): FAQ said "we ship to Poland and the UK" in PL/EN/NL → now incl. the Netherlands
  (source + en/nl translations; backups faq.original.*.html).
- Theme copy "Niaali - NL (werk)" #208277143884 (unpublished, copy of live "Fabric - Product page v2"), in nl/:
  snippets/pp-local-url.liquid puts web-address menu links to /apps/… (order tracking, ParcelPanel) in the visitor's
  folder (/nl-nl, /en-gb); used in header menu, mega menu, mobile drawer and footer menu. BLIK payment icon hidden
  outside Poland (blocks/payment-icons.liquid).
- Owner to do in apps/admin: Kaching Cart texts per language (drawer is Polish: "Twój koszyk", "Dodaj jeszcze…",
  "Oszczędzasz", "Dodaj do koszyka", "Rabaty", "Razem", "PRZEJDŹ DALEJ", "armowa dostawa" missing D, empty state
  in English); Swatch King: add option name "Kleur" to the colour (image) preset so NL gets photo swatches like
  PL/GB; Shopify Payments: enable iDEAL for NL; optional: Dutch URL handles, Polish image alt texts.

## Without Kaching Cart and Swatch King (theme copy "Niaali - NL (werk)" #208277143884, 2026-10-18)
Built in nl/theme (originals in nl/orig). Tested in preview on PL, NL and GB, mobile and desktop.
- Swatches: colour options (kolor/kleur/color/… any language) render square photo swatches from the variant image
  (snippets/variant-main-picker, swatch, pp-color-hex with PL/NL/EN colour names as fallback and the CSS);
  works on the product page and in the theme quick add. Swatch King embed switched off in this copy.
- Cart (theme drawer + cart page, Kaching Cart embed switched off in this copy): tier bar at the top
  (pp-tier-progress, now also rendered on the server so it is never empty after a redraw), compact upsell rows
  "Complete your look" from the shopper's group collection (pp-cart-upsell + pp-card-data), "You save €X" and
  free shipping · 60-day returns · secure checkout under the total (pp-cart-extras), texts via pp-i18n.
- pp-quick-pick adds via /cart/add.js with the cart sections and fires the theme CartAddEvent (drawer redraws and opens).
- Shopify discounts created, scheduled for 2027-01-01 (not active yet), same tiers as Kaching:
  MIX & MATCH -10% (2+) gid://shopify/DiscountAutomaticNode/2289031053644,
  -15% (3+) …/2289031086412, -20% (4+) …/2289031119180.
### Switch (one moment)
1. Owner publishes "Niaali - NL (werk)".
2. Set the three MIX & MATCH discounts to start now (Claude can do it).
3. Owner turns off the Kaching Cart discounts in the app (or Discounts → "Kaching Cart - … V2" → deactivate).
4. Test one order on /nl-nl; after a few days uninstall Swatch King (can go right after publishing) and Kaching Cart.
### Switch done (2026-10-18)
- "Niaali - NL (werk)" #208277143884 is live (published by the owner).
- Kaching Cart discounts (Order/Shipping/Product V2) deactivated; MIX & MATCH -10/-15/-20% active from 16:38 UTC.
- Live test on mobile, 1–4 items, PL (PLN), NL (EUR) and GB (GBP): 0/10/15/20% applied with the right MIX & MATCH
  title; tier bar in the local language; checkout NL in Dutch, € total discounted, free shipping.
- Still open: iDEAL not yet shown at NL checkout (owner enables it in Shopify Payments).
- Swatch King uninstalled by the owner (2026-10-18). Live check PL/NL/GB, mobile and desktop: square photo
  swatches from the theme code, colour name updates on click, no leftover app code, no script errors.

## Black Friday (2026-10-31, user GO: same as Davento, slightly different look, keep red + black, own cart)
Draft theme "Black Friday" #209387651404 = duplicate of live "Niaali - size guide (live) 29 Oct" #209223450956.
Playbook: davento/black-friday/PLAYBOOK.md. Work files: niaali/black-friday/.
- LIVE STORE gifts (same as Davento, 84,95 zł ≈ €19,95): Apaszka Marina (prezent-apaszka-marina, 16260116578636),
  Etui na Karty (prezent-etui-na-karty, 16260116611404) – women; Portfel Klasyczny (prezent-portfel-klasyczny,
  16260116644172), Bransoletka Pancerka (prezent-bransoletka-pancerka, 16260116676940) – men. Tags regalo +
  regalo-donna/regalo-uomo (same tags as Davento so the theme code is shared), type Prezent, not tracked, active,
  Online Store channel only (not Google/Shop), seo.hidden, in no collection, NL/EN translated, Davento photos.
- LIVE STORE discount "Free Gift" (gid://shopify/DiscountAutomaticNode/2291414761804): buy ≥ 349 zł from Kobiety or
  Mężczyźni, 1 gift 100% off, once per order, combines with product/order/shipping discounts.
- MIX & MATCH -10/-15/-20% still ACTIVE on purpose: the live theme still advertises it. Deactivate when the Black
  Friday theme is published (ids 2289031053644 / 2289031086412 / 2289031119180).
- LIVE STORE collections (sold ≥1 in 120 days, summer items left out; list data/bestsellers-120d.txt):
  Bestsellery Damskie (bestsellery-damskie, 72), Bestsellery Męskie (bestsellery-meskie, 73), Bestsellery
  (bestsellery, sub-collections of both, 145), Best selling sort, all 4 channels, NL/EN titles.
  Main menu: "Bestsellery" after Strona główna (NL/EN Bestsellers). Backup: black-friday/orig/main-menu.json.
- Free Gift discount minimum lowered to 339 zł (shown: 349 zł PL, €80 NL, £70 UK). Rates in the preview: EUR 0.2271,
  GBP 0.1930 per zł → 349 zł would be €79.26 / £67.34, too close to €80 / £70; at 339 zł (≈ €77 / £65) the gift is
  always free when the theme lets a customer pick it. PL market prices are +10% (gift shows 93,45 zł in PL).
- THEME (draft #209387651404), all in niaali/black-friday/theme (originals in orig/):
  - Gift system: snippets/pp-gift-min (34900 PLN; local EUR 8000, GBP 7000), pp-gift-text (pl/nl/en),
    pp-gift-cart (markup), pp-gift-script (one script per page, from the header group: Fabric morphs the drawer and
    does not run scripts inside it; uses @theme/events CartUpdateEvent + cart sections to redraw).
  - sections/pp-gift-showcase in header-group after the header: beige gift bar + palette (:root --pp-*, ink #121212,
    beige #edebe7, red #c20000, champagne #d8c3a5) + title font Cormorant (cormorant_n6) for h1/h2/pp titles +
    red "Bestsellery" menu tag (snippets/pp-bf-header) + end date snippets/pp-bf-active (1 Dec 2026, 00:00 PL).
  - Announcement bar: Halloween and Mix & Match messages disabled; free shipping + 60-day returns remain.
  - Home: sections/pp-bf-hero first (typographic, red + champagne ribbons, Cormorant, PL/NL/EN, Kobiety/Mężczyźni,
    link "Zobacz bestsellery" → bestsellery); Halloween hero disabled (kept).
  - Badge "BLACK FRIDAY" (straight red label, top-left) on every pp-card and the first product photo
    (snippets/pp-bf-badge; product page via CSS from the benefits block).
  - Gift line instead of the tier bar: home bestsellers, collection head, product cross-sell; cart drawer + cart page
    gift block (pick/swap, max 1, removed under the minimum). Cross-sell title "Uzupełnij zamówienie" (pp-gift-text).
  - Collection head: chips Wszystko | Damskie | Męskie on the 3 Bestsellery collections (NL Alles/Dames/Heren).
  - Product page: third bullet = personal gift line (variant + cart vs minimum; Fabric variant:update/cart:update);
    "Łącz i oszczędzaj" tab → "Prezent gratis" with blocks/pp-gift-tab (PL/NL/EN text; tab heading itself is a
    template setting: NL/EN translation still to add in Translate & Adapt / T-Lab); new blocks PP Rating (above the
    title) and PP Stock (above buy buttons), both disabled.
  - Cart: no quantity selector (bin icon removes), "Oszczędzasz X" without the gift's price.
  - Checkout line (locales pl/nl/en): "Tylko 3% klientów skorzystało z gwarancji zwrotu pieniędzy" (refunds 2.5%
    of sales, 60 days).
  - Tested in preview (PL mobile + desktop, /nl-nl, /en-gb): gift bar 349 zł / €80 / £70, hero, red menu tag, badge,
    product gift line (68,55 zł / € 22,05 left), chips, cross-sell title, cart pick → "Twój prezent: Apaszka Marina ✓".
    Gift NOT €0 yet in the cart while MIX & MATCH is active (Shopify applies the bigger Mix & Match discount instead
    of combining) → deactivate Mix & Match when publishing.
- Feedback round 1 (user): menu under the logo (header menu_row bottom, centred); hero offer in Geist bold (Cormorant
  had sinking figures), "Black Friday" on one line and centred on phones; trust row smaller (22px icons, 12px text,
  56px apart on desktop, 2x2 on phones); categories = bestsellers (5 per row, 262x328 desktop / 164x205 mobile, both
  4:5, same left edge); titles Playfair Display 700 (also FAQ / text headings); cart: "Oszczędzasz −X" red line +
  "Darmowa dostawa · Zwrot 60 dni · Bezpieczna płatność" on one line; gift photos 192px (sharp).
- Fix: blocks/pp-rating.liquid and blocks/pp-stock.liquid had never been uploaded, so templates/product.json (which
  references them) was silently rejected – no rating/stock blocks, no "Prezent gratis" tab until now. Uploaded; the
  product template now has PP Rating (above the title) and PP Stock (above buy buttons), both OFF like Davento, and
  the gift tab. Lesson: after every upsert check checksum/updatedAt of EVERY file, JSON templates too.
- "O nas" photo (user): Cozy_Christmas_Couple_Portrait_1.png in the about section of home, product page and the
  O nas page hero (page.about). Legacy templates product.sale-pdp / product.shoes-pdp (no product uses them) refuse
  any save (old invalid content) – left as they are.
- Category photos scaled 4% (hides thin black edges inside some category image files). Footer column titles in
  Playfair Display too.
- Test templates created while debugging (delete in Edit code): templates/product.t2.json, product.t3.json,
  product.t4.json, product.tc.json.
- Round 2 (user): category photos show the whole model (no zoom, top-aligned; only the kurtki photo with a black edge
  in the file is zoomed 3%); "O nas" compact on every page (phone photo 4:3 ≈ 290–380px, title 34px; desktop photo
  560px, title 56px); PP Rating moved to the top of the product details list (still off) so it is easy to find in
  the editor, PP Stock above buy buttons (off); delivery line ("Wysyłka w ciągu 1–2 dni roboczych") off; product
  title 4px under the photo on phones; gift products (tag regalo) never shown in cross-sell, home bestsellers or
  cart add-ons.
