# Stellamea (www.stellamea.com) – analysis before the kit (2026-10-05, no changes made)

- Shop uvuk2u-pc, Spain only, EUR, Spanish only, taxes included, not Plus. 245 active / 11 draft products.
- Live theme "Stellamea" #196272292184 = Dwell preset (same base as NewMae → NewMae kit ports 1:1).
- Fonts Manrope (body) + Epilogue (headings); palette white / #4A4A4A / terracotta #7D5449 / linen #EDEBE7 / navy footer.
- Custom CSS hides compare-at prices, sale badge and cart tax note. No discounts. Tracking app WeTracked (leave as is).
- Checkout: card (+2), PayPal, Klarna, express. Shipping rate "Free Shipping" (English), ES only, free.
- Policies (Shopify policies, Spanish): shipping 1–2 + 3–7 = 4–9 business days, free, tracked. Refund policy: 30 days,
  customer pays return shipping unless faulty/wrong, no restocking fee, refund within 7 business days, NO exchanges.
  Support Mon–Fri 09–17, reply within 12 business hours. Company Auremir, Cano y Cueto 7-A, 41004 Sevilla.

## Issues found
1. Returns 30 days (refund policy) vs 60 days (legal notice) – contradiction.
2. Email links: href="support@stellamea.com" without mailto (broken) in contact/legal/privacy/refund/shipping/terms;
   payment policy + desistimiento page link to support@auremir.com.
3. Privacy policy says "Stellemea"; legal notice says reply within 1 business day vs 12 business hours elsewhere.
4. English texts in the store: "Cart", "DISCOVER SOMETHING NEW", "You might also like...", rate "Free Shipping".
5. Footer menu "footer" (not used in footer?) links to non-existing pages /pages/contacto, informacion-de-pago,
   declaracion-de-desistimiento. Pages sobre-nosotros, preguntas-frecuentes, contactanos have an empty body.
6. Small collections in the menu: Bolsos 1, Bañadores 1, Pijamas 1, Accesorios 1, Conjuntos 2, Monos 2, Hombre Bolsos 1.
7. Home is women-only (Hombre = 118 products not shown); "Prendas seleccionadas" shows 1 product.
8. Spain/Omnibus: a strike-through "before" price must be the lowest price of the last 30 days → no red sale box
   unless prices are real; urgency via bundle discounts instead.

## Done (2026-10-05, after GO)
- Pages fixed (links only): Política de Pagos + Formulario de Desistimiento → mailto:support@stellamea.com.
- Shipping rate renamed "Free Shipping" → "Envío gratuito con seguimiento".
- Automatic discounts: Compra 2, ahorra 10% (2222800929112) · Compra 3, ahorra 15% (2222800961880) ·
  Compra 4+, ahorra 20% (2222800994648). Verified on the live cart (1 → 0%, 2 → 10%, 3 → 15%, 4 → 20%).
- Work theme "Stellamea - kit (werk)" #199421821272 (copy of live, unpublished).
- Policies: API has no write_legal_policies scope → corrected texts in stellamea/policies/*.html to paste in
  Settings → Policies (30 days everywhere, exchanges allowed, mailto links, Stellemea typo, 12 business hours).
- Compare-at: 170 of 245 active products have a compare-at price (34 of them more than 40% off). User keeps an eye on it.

## Kit in work theme "Stellamea - kit (werk)" #199421821272 (not published)
- Files in stellamea/theme (Alove kit base, identical Horizon/Dwell base files). Everything in Spanish (tú, Spain wording:
  "Añadir al carrito"), texts follow the policies: free shipping Spain, 1–2 days processing, 4–9 business days total,
  30 days returns + exchanges (size/colour), refund within 7 business days, support@stellamea.com, 12 business hours.
- Look: terracotta #7D5449 + linen #EDEBE7, navy footer kept; Lora headings + Manrope body; square linen trust tiles;
  terracotta check marks; pill tier bar "2 · −10% / 3 · −15% / 4+ · −20%"; red sale pill; round photo swatches;
  underlined tabs; FAQ two columns on desktop; sticky header; terracotta announcement bar (3 messages).
- New: delivery window under the button ("Recíbelo entre el 9 y el 16 de octubre"), business days 4–9, weekends skipped.
- Compare-at prices visible again (custom CSS that hid them is not in the kit settings). Cart total without "EUR".
- FAQ page template: 8 questions (incl. exchanges) with working email. Chips/categories drop the "Mujer "/"Hombre " prefix.
- Checkout texts in locales/es.json: "o paga de forma segura abajo", free tracked shipping messages.
