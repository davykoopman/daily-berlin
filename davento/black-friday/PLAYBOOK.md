# Black Friday playbook – alles wat in Davento is gedaan

Bron: Davento (davento.it), concept-theme "Black Friday" #208380952919 (kopie van de live theme), 30–31 okt 2026.
Doel: dezelfde aanpak in een andere store. Eindstand per onderdeel; wat de eigenaar heeft afgekeurd staat onderaan
bij "Niet doen". Bestanden staan in `davento/black-friday/theme/`, originelen in `davento/black-friday/orig/`.

Legenda: **[THEME]** = alleen in de concept-theme (live na publiceren) · **[STORE]** = direct live in de winkel
(producten, collecties, kortingen, menu, pagina's).

---

## 0. Werkwijze en regels

- Altijd in een **kopie van de live theme** werken; de eigenaar publiceert zelf. Live theme blijft als rollback.
- Geen wijziging zonder GO; eerst voorstel + screenshot/mockup.
- Elke tekst per taal (IT/DE/FR/EN) in de code; geen tekst in afbeeldingen (meerdere markten).
- Geen nep social proof, geen nep urgentie, geen nep-bedragen. Tracking/pixels niet aanraken.
- Altijd testen: mobiel (375/390px) + desktop (1440px), elke markt (IT, /de-de, /en-gb, /de-ch).
- Voor het overschrijven van `templates/*.json` of `sections/header-group.json`: eerst kijken of de eigenaar in de
  editor iets heeft veranderd en die wijzigingen meenemen.
- Eén einddatum voor alles wat Black Friday-specifiek is: `snippets/pp-bf-active.liquid` (1 dec 2026 00:00
  Italiaanse tijd). Daarna verdwijnen lint, rode menuknop enz. vanzelf.

## 1. Kleuren en typografie [THEME]

- **4 kleuren**, één plek (`:root` in `snippets/pp-card.liquid` én in `sections/pp-gift-showcase.liquid`, want die
  staat op elke pagina):
  - ink `#1c1d1d` (alle tekst, knoppen zwart), wit `#ffffff` (pagina), crème `#f3efe8` (alle zachte vlakken),
    rood `#c20000` (alleen korting/Black Friday). Lichtere tinten = ink met transparantie, nooit een nieuwe kleur.
  - Theme-instellingen omgezet: tekst/header/drawer/footer `#1c1d1d`, randen `#e4e4e4`, sale-kleuren `#c20000`,
    kapotte custom CSS (groene sale-prijs) → rood. Sale-prijs rood, oude prijs en gewone prijs ink.
  - Les: de kleurvariabelen moeten op **elke** pagina geladen worden (anders zijn contact/FAQ/over-ons kleurloos).
- **Alle titels in DM Serif Display**, sentence case, geen hoofdletters, geen letterafstand: font picker
  "Title font (all pages)" in `pp-gift-showcase` zet h1/h2/.h1/.h2, producttitel, collectietitel, home- en
  cross-sell-titels. Theme-instelling header font niet aangeraakt. Footer-koppen volgen mee.
- Producttitel op mobiel: 20px, max 2 regels (langer → …), marge 0 0 6px (`pp-gallery-nav`). Desktop ongewijzigd.

## 2. Header, menu en balken [THEME + STORE]

- **Header wit** (donkere header afgekeurd). Alleen de menuknop naar de Bestseller-collectie is een **rode pil**
  zolang de actie loopt (`snippets/pp-bf-header.liquid`, geladen vanuit `sections/pp-announcement.liquid`); in het
  mobiele menu rood + vet. Geen "-50%" in de pil.
- **Aankondigingsbalk** (`pp-announcement`): 2 berichten wisselen: gratis verzending · retour binnen 60 dagen
  (IT/DE/FR/EN). Geen kortings-/tierteksten meer.
- **Cadeaubalk onder het menu op elke pagina** (`sections/pp-gift-showcase.liquid`, in `sections/header-group.json`
  direct na de header): smalle crème balk (45px desktop / 41px mobiel), rood cadeau-icoon + "Regalo gratuito per
  ordini sopra €80" + de 4 cadeaus als foto's van 32px (26px mobiel). Mobiel korte tekst ("Regalo gratuito sopra
  €80") zodat het op één regel blijft.
- **[STORE] Menu**: item "Bestseller" na Home (geen subitems), vertaald EN Bestsellers / DE Bestseller /
  FR Best-sellers. Back-up van het menu vooraf: `orig/main-menu.json`.

## 3. Homepage [THEME]

Volgorde: hero → trust-rij → categorieën → bestsellers → Chi siamo (tekst + foto) → FAQ.
Oude slideshow (Halloween) uitgezet, niet verwijderd (rollback).

- **Hero** (`sections/pp-bf-hero.liquid`):
  - Eigen foto + Black Friday-blok, tekst als HTML (vertaalbaar). Desktop naast elkaar, mobiel foto boven.
  - Kicker "TUTTO NOVEMBRE" (zonder winkelnaam), brons `#d6a874`; titel wit in DM Serif Display; aanbod rood
    ("fino al -50%"; instelling "up to"/vast percentage).
  - Linten onderaan: rood + brons-goud verloop; **satijnglans** (witte streep) loopt elke 7 s over de linten en het
    aanbod. Geen goud elders op de site, geen gouden rand om het aanbod.
  - **Openingsanimatie** (1×, alleen CSS): kicker/titel direct zichtbaar en schuiven 16px op, aanbod "stempelt" in op
    0,5 s, sub + knoppen op 0,85/0,95 s. Uit bij "reduced motion". Vertraagt LCP niet.
  - Knoppen naar Donna/Uomo (gelokaliseerde links) + klein bronzen linkje "Scopri i bestseller →"
    (DE Bestseller entdecken, FR Voir les best-sellers, EN Shop bestsellers) naar de Bestseller-collectie.
- **Trust-rij tijdens Black Friday** (`sections/pp-trust.liquid`): één witte rij, fijne ink-iconen, kleine titels in
  hoofdletters, dunne scheidingslijnen, mobiel 2×2. Na 1 dec automatisch de normale trust-rij.
- **Titels**: "Shop per categoria" / "I più venduti" (vertaald), DM Serif 34px (26px mobiel), geen rode tekst erboven
  (`snippets/pp-gender-tabs.liquid` + beide secties).
- **Categorieën** (`pp-home-categories`): 5 per rij desktop, foto's volledig in 2:3 (geen halve hoofden), "bekijk
  alles"-tegel ook 2:3, pijlen midden op de foto. Tablet 3 per rij, mobiel swipen. Nieuwe categoriefoto's in 2:3.
- **Bestsellers** (`pp-home-best`): 5 per rij, foto's 4:5, cadeauregel i.p.v. kortingsbalk.
- Categorieën, bestsellers, collectie- en productpagina-rijen gebruiken dezelfde kaart, maat, tussenruimte (12px
  desktop / 10px mobiel), pijlen en 14px rand op mobiel.

## 4. Productkaarten en lint [THEME]

- **Rood hoeklint "BLACK FRIDAY"** (`snippets/pp-bf-ribbon.liquid`) op alle productkaarten (96px, 72px mobiel) en op de
  productfoto (150px / 120px mobiel). Alleen de tekst "BLACK FRIDAY", geen percentage. Niet in de afbeeldingsbestanden
  (Google Shopping blijft schoon). Niet op categorietegels. Verdwijnt vanzelf op 1 dec.

## 5. Collectiepagina's [THEME + STORE]

- Kop (`sections/pp-collection-head.liquid`): titel gecentreerd, cadeauregel gecentreerd eronder, categorieknoppen
  uit het menu (mobiel één swipe-rij vanaf links).
- **Bestseller-pagina's** krijgen eigen knoppen **Tutto | Donna | Uomo** (DE Alle/Damen/Herren, FR Tout/Femme/Homme,
  EN All/Women/Men); op mobiel gecentreerd als ze passen.
- **[STORE] Bestseller-collecties**: alle producten met ≥2 verkopen in de laatste 120 dagen (badjas/bh eruit),
  gesplitst op donna/uomo/unisex in de titel → Bestseller Donna (123) en Bestseller Uomo (126), sortering
  "Best selling". "Bestseller" = beide als subcollecties (248, blijft in sync). Gepubliceerd in dezelfde kanalen als
  Donna/Uomo; titels en beschrijvingen vertaald (DE … Damen/Herren, EN Bestsellers Women/Men, FR Best-sellers
  Femme/Homme). Handles blijven `black-friday(-donna/-uomo)`. Let op: Donna/Uomo zijn een vaste lijst, na de actie
  verversen. Productlijst: `data/bestsellers-120d.txt`.

## 6. Productpagina [THEME]

- Volgorde blokken: (rating) → titel → prijs (sale rood + oude prijs + "-50%") → 3 bullets → kleur → maten → knoppen
  → tabbladen → cross-sell.
- **3 bullets** (`snippets/pp-benefits.liquid`): gratis verzending · tevreden of geld terug binnen 60 dagen ·
  **cadeauregel** (rood icoon, vet), persoonlijk: dit product + mandje tegen de drempel → "Regalo gratuito incluso ✓"
  of "Ancora €17,05 per un regalo gratuito"; volgt variant en mandje; bullets netjes bovenaan uitgelijnd.
- **PP Rating** en **PP Stock** als losse blokken (`sections/main-product.liquid`, `snippets/product-template.liquid`,
  `snippets/pp-rating.liquid`, `snippets/pp-stock.liquid`), standaard UIT, aan/uit met het oogje in de editor:
  - Rating: altijd boven de titel; bron Handmatig (4.7, 2000 klanten, vertaalde tekst) of review-app (metafields).
    Alleen met echte cijfers.
  - Stock: pulserende stip + "Disponibile, pronto per la spedizione", geen voorraadlogica (eigenaar: "risico op mij"),
    verborgen bij uitverkochte variant, notitie eronder uit.
- Galerij (`snippets/pp-gallery-nav.liquid`): thumbnails weg, stipjes op de foto, pijlen bij hover op desktop.
  Mobiel: foto volledig schermbreed, kolom exact 14px rand (theme gaf 3px extra), **maten op één regel**
  (gelijke breedte, 13px).
- Blokafstand 25 → 16px (titel 10px). Blok "Spedito entro 1–2 giorni" uit. **Sticky add-to-cart** aan.
- Tabblad "Regalo gratuito" i.p.v. bundeltabblad (`snippets/pp-product-info.liquid`).
- Cross-sell (`sections/pp-bundle.liquid`): titel "Completa il tuo ordine" in DM Serif + cadeauregel.

## 7. Winkelmandje (drawer) [THEME]

Volgorde: cadeaublok → producten → "Completa il tuo look" → totale besparing → totaal → perks → afrekenknop.

- **Geen aantal-kiezer** op de hele site (`snippets/cart-item.liquid`); klein "Rimuovi"-linkje i.p.v. (gebruikt de
  verborgen min-knop zodat de drawer direct bijwerkt).
- **Cadeaublok** (`snippets/pp-gift-cart.liquid`): onder de drempel "Ancora €X…" + voortgang + cadeaus op slot; vanaf
  de drempel kiezen (tik = toevoegen, €0,00), wisselen kan, max. 1 cadeau, onder de drempel automatisch eruit.
- **"Completa il tuo look"** (`snippets/pp-cart-upsell.liquid`): fototegels 4:5 met rond zwart "+" en alleen de prijs;
  3 per rij desktop, 2,6 mobiel (derde tegel piept, dus duidelijk swipebaar). Kiest donna/uomo op basis van het mandje.
- **Totale besparing** boven het totaal, rood en vet: "Risparmi in totale / Du sparst insgesamt / Vous économisez /
  You save −X" = (doorgestreepte of oude prijs − betaald) × aantal + kortingscodes. Cadeaus tellen niet mee, geen
  cadeautekst. Verborgen bij €0.
- **Perks** klein (11px tekst, 13px iconen): gratis verzending · retour 60 dagen · veilig betalen.

## 8. Checkout [THEME]

- Tekst "oppure paga in modo sicuro qui sotto" → "Solo il 3% ha usato la nostra garanzia soddisfatti o rimborsati"
  (it/de/en/fr locales). Echt cijfer: 54 refunds op 1.940 orders = 2,8% → 3%.

## 9. Gratis cadeau i.p.v. stapelkorting [STORE + THEME]

- **Waarom**: stapelkorting (2/3/4 = 10/15/20%) kostte direct 10%+ (€5.450 in 60 dagen); cadeau kost ±€1–1,50.
- **[STORE] Stapelkorting** (Mix & Save) gedeactiveerd, niet verwijderd.
- **[STORE] 4 cadeauproducten**: €19,95, korte namen (Foulard Marina, Portacarte Nero – dames; Portafoglio Classico,
  Bracciale Grumetta – heren), tag `regalo` + `regalo-donna`/`regalo-uomo`, type Regalo, voorraad niet bijhouden,
  actief + gepubliceerd (nodig voor het mandje), verborgen voor zoeken (`seo.hidden`), in geen enkele collectie,
  vertaald (EN zonder €-bedrag). Leverancier ziet ze gewoon in de order.
- **[STORE] Automatische korting "Free Gift"** (Buy X get Y): min. €80 uit de collecties Donna of Uomo, 1 van de 4
  cadeaus 100% gratis, 1× per order, combineerbaar met product-/order-/verzendkortingen. Titel is niet vertaalbaar.
- **[THEME] Eén bron** `snippets/pp-gift-min.liquid` (handles + drempel) en `snippets/pp-gift-text.liquid` (alle
  teksten IT/DE/FR/EN). Overal zichtbaar: balk onder menu, productpagina-bullet + tabblad, cross-sell,
  collectiekop, home bestsellers, mandje.
- **Drempel per valuta**: euro €80 · UK **£70** · Zwitserland **80 CHF** (vaste ronde bedragen, iets boven de
  omgerekende €80, zodat de korting altijd werkt); andere valuta = €80 omgerekend en naar boven afgerond.
- Getest: €0-cadeau, wisselen, automatisch verwijderen, checkout €117,85 → €97,90.

## 10. Pagina's [THEME]

- **Over ons** (`sections/main-page.liquid` + `templates/page.json`): grote foto boven de tekst (16:9 desktop, 4:3
  mobiel, instelbaar in de editor; tijdelijk de kerstfoto), foto uit de paginatekst weggelaten (alle talen), tekst in
  een kolom van 680px met grotere eerste zin, alt-tekst per taal. Contact/FAQ/betalen ongewijzigd.

## 11. Analyse vooraf (alleen advies)

- 88% mobiel; mobiele ATC 5,1%, checkout bereikt 65% van ATC, conversie 1,44%; AOV €65.
- Snelheid (mobiel, traag 4G): LCP product 1,8 s, home 1,7 s; late "LCP" 4–5 s = cookiebanner. Afbeeldingen onder
  de vouw laden al lazy. Pixels/tracking niet aangeraakt.
- 3 topverkopers stonden op concept (cargo uomo, completo uomo occasioni speciali, completo donna eleganti) → navragen.
- Prijzen: EU-regel laagste prijs 30 dagen geldt voor de aangekondigde korting.

## 12. Niet doen (afgekeurd door de eigenaar)

- Donkere header, goud buiten de hero, gouden rand om het aanbod, rode kicker-tekst boven titels.
- Bewegende tape/ticker in de trust-rij ("te druk"), crème kaartjes in de trust-rij.
- Percentage in het productlint of in de menuknop ("-50%").
- Grote cadeausectie op de home ("veel kleiner") → smalle balk onder het menu.
- Notitie onder de voorraadregel; aantal-kiezer in het mandje; veel tekst in de cross-sell tegels.
- Cadeauwaarde (€19,95) meetellen als besparing of cadeautekst in het mandje.

## 13. Checklist voor de volgende store

1. Live theme dupliceren → "Black Friday"; originelen bewaren.
2. Store-feiten ophalen uit de eigen policies: verzendkosten, retourtermijn, e-mail, markten/valuta/talen.
3. Data: AOV, mobiel-aandeel, refundpercentage (voor checkouttekst), bestsellers laatste 120 dagen, concepten.
4. Palet (4 kleuren) + titelfont bepalen (zelfde structuur, andere look per store).
5. Hero, trust-rij, lint, header-pil, einddatum in `pp-bf-active`.
6. Cadeauproducten aanmaken + korting "Free Gift" + drempel per valuta in `pp-gift-min`; oude stapelkorting uit.
7. Bestseller-collecties (alles/dames/heren) + menu-item + vertalingen.
8. Productpagina, mandje, checkouttekst, over-ons-pagina.
9. Testen per markt, mobiel + desktop; daarna publiceert de eigenaar.
10. Na de actie: Bestseller Donna/Uomo verversen, over-ons-foto terug, kerstfoto's eruit.

## Open punten Davento (door de eigenaar)

- `templates/product.pp-test.json` en `assets/pp-logo-white.png` verwijderen (Edit code).
- Menuvertalingen: DE "Frau/Mann" → Damen/Herren, EN "Woman/Man" → Women/Men.
- Frans: vertalingen staan klaar, maar er is geen markt waar Frans zichtbaar is.
- Na publiceren: live theme toont geen stapelkortingsteksten meer (die korting staat al uit).
