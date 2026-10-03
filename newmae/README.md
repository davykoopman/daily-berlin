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
