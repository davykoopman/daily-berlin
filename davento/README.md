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
- Footer menu "Politiche": added "Note legali" → /policies/legal-notice (after "Condizioni di servizio").
- Page "Domande Frequenti": "in Italia e Germania" → "in Italia, Germania e Svizzera" (free shipping
  answer and "Spedite anche all'estero?" answer, which was "soltanto in Italia e Germania").
- Page "Pagamenti": "Accettiamo pagamenti in EUR (€) tramite…" → "…in EUR (€) e, per gli ordini in Svizzera,
  in franchi svizzeri (CHF) tramite…". TWINT not listed yet (add once it is active).
- Open: legal notice needs owner name + legal form (API has no write_legal_policies, user pastes);
  shipping policy still says Italy and Germany only; homepage FAQ block in the live theme still says
  "Italia e Germania" (live theme can't be written via API); German translations of the changed pages.
