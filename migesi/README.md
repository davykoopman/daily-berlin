# Migesi (www.migesi.com) – Black Friday

Earlier history (Alove Fashion → Migesi rebrand): alovefashion/README.md.
Store: UK only, GBP, English. Live theme "Migesi - size guide (live) 29 Oct" #203864473947 (Horizon).
Playbook: davento/black-friday/PLAYBOOK.md. Closest port: niaali/black-friday (Horizon family).
User GO (1 Nov): same as Davento + Niaali, same free gifts, bundle (stacking) discount off, offers up to 70%
(the user sets the product discounts once the draft theme is ready). Wants to see every step; web + mobile.

## Black Friday – store (live, 1 Nov)
- Draft theme "Black Friday" #204029624667 = duplicate of the live theme. Originals of the files I change:
  black-friday/orig/.
- Gifts (same as Davento/Niaali, Davento photos), £17.95 each, type Gift, vendor Migesi, tags regalo +
  regalo-donna / regalo-uomo, not tracked, no SKU, active, Online Store only, seo.hidden = 1, in no collection:
  Marina Scarf (gift-marina-scarf, 10851646964059), Card Holder (gift-card-holder, 10851647062363) – women;
  Classic Wallet (gift-classic-wallet, 10851647095131), Curb Chain Bracelet (gift-curb-chain-bracelet,
  10851647127899) – men.
- Discount "Free Gift" (gid://shopify/DiscountAutomaticNode/1949136978267): spend £70 on WOMEN or MEN, 1 gift
  100% off, once per order, combines with product/order/shipping discounts, 1 Nov 00:00 UTC → 1 Dec 00:00 UTC.
- Bundle discounts "Buy 2 save 10%" (1939658015067), "Buy 3 save 15%" (1939658047835), "Buy 4+ save 20%"
  (1939658080603) still ACTIVE on purpose (live theme advertises them) → deactivate when the Black Friday theme
  is published.
- Collections (sold ≥1 in the last 120 days; summer items, drafts, out of stock left out; data/bestsellers.json):
  Bestsellers Women (bestsellers-women, 18), Bestsellers Men (bestsellers-men, 23), Bestsellers (bestsellers,
  sub-collections of both, 41). Best selling sort, all 4 channels.
- Main menu: "Bestsellers" after Home. Backup: black-friday/orig/main-menu.json.

## Black Friday – theme (draft "Black Friday" #204029624667, not published)
All changed files in black-friday/theme (originals in black-friday/orig/). Ported from Niaali (Horizon family) and
Davento lessons; Migesi look: deep green ink #1f2a1f, Migesi cream #f6f2eb, the store's own sale red #a8231b,
champagne only in the hero; titles Playfair Display 700 (also about/footer headings; product description headings
stay regular). English only, GBP, £70.
- Gift system: snippets/pp-gift-min (£70, 4 gift handles), pp-gift-text (EN), pp-gift-cart (markup), pp-gift-script
  (fast pick from Niaali v2 + Davento v2: optimistic, ONE /cart/update.js, last click wins, gift photos stay in place).
  This Horizon version has no CartUpdateEvent: the script dispatches the standard 'shopify:cart:lines-update'
  (CartLinesUpdateEvent from @shopify/events, promise resolved with the update.js cart + sections) so drawer, cart
  page and cart bubble redraw; it listens to the same event for the theme's own adds/removes.
- sections/pp-gift-showcase in header-group after the header: cream gift bar + palette + title font + red
  "Bestsellers" menu tag (pp-bf-header) + end date pp-bf-active (1 Dec 2026 00:00 UK = discount end).
- Announcement bar: Halloween + "Mix & save" off; free UK delivery + 14-day returns stay.
- Home: pp-bf-hero first ("Up to 70% off", Jost bold offer, Women / Men / Shop bestsellers); Halloween hero off;
  trust row compact (36px round icons); bestsellers 5 per row from bestsellers-women / -men (no summer items).
- Badge "BLACK FRIDAY" on cards and the first product photo; gift line instead of the tier bar (home bestsellers,
  collection head, product cross-sell "Complete your order"); chips All | Women | Men on the 3 bestseller collections.
- Product page: third bullet "Free gift with orders over £70"; accordion "Mix & Save" → "Free gift" (pp-gift-tab);
  PP Rating (top, OFF, rating 0 = shows nothing until real numbers are entered) and PP Stock (above buy buttons, OFF);
  delivery line off.
- Cart (drawer + page): gift block on top, no quantity selector, bin on the right under the price, "Free Gift"
  discount name hidden (£0.00 says it). Under the total (snippets/tax-info, was the bundle tier bar): "You save £X"
  (gifts not counted) + Free UK delivery · 14-day returns · Secure checkout.
- Tested in preview (1 Nov, mobile 390 + desktop 1440): 13 pages each, no Liquid/JS errors from the theme, no
  horizontal scroll, no Halloween / Mix & save / 50% / Polish text. Flow: under £70 "£39.05 more for your free gift",
  gifts locked; over £70 pick → line at £0.00 in ~1 s (UI instant), 3 rapid swaps → exactly 1 gift (the last),
  drawer pick works, removing an item below £70 removes the gift automatically.
- At publish: deactivate the 3 bundle discounts (with them active Shopify gives Buy-2/3 instead of combining once
  the gift is gone; seen in the test: £73.71 after removing the gift).
- Round 2 (user feedback, 1 Nov):
  - Product page on phones: photo directly under the gift bar (section top padding 0 on phones; was a 21px white strip).
  - PP Stock: Migesi's product details have a 12px gap (Niaali 28px), so the -16px pull made the line overlap the
    button → -4px (12px under sizes, 8px above the button, dot centred). Switched ON in the draft (user turned it on).
  - PP Rating: shows nothing while the rating is 0 (no real numbers yet); in the theme editor a dashed hint says to
    fill in the real rating + number of customers. Pull to the title -6px.
  - Footer on phones: every column on the same 16px left edge (group-block / menu details padding removed).
  - Cart add-ons "Complete your look" (snippets/pp-cart-upsell + pp-card-data from Niaali) in drawer and cart page,
    from bestsellers-women / -men, "+ Add" opens the quick pick sheet; no gifts, nothing already in the cart.
  - Checkout line (locales/en.default.json, shopify.checkout.alternative_payment_method_banner.or):
    "or pay securely below" → "Only 3% of our customers returned their order". Checked: 2 of 69 orders refunded in
    the last 365 days (2.9%), £85.90 of £3,505.49 sales returned (2.5%).
  - Live theme still shows Halloween (announcement + hero): writes to the live theme are blocked for the API → owner
    switches it off in the editor (or publishes the Black Friday theme).
