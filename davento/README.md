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
