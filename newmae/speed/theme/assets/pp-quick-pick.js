(function () {
  if (window.ppQuickPick) return;
  window.ppQuickPick = true;

  var i18nEl = document.querySelector('[data-pp-qp-i18n]');
  var i18n = i18nEl ? JSON.parse(i18nEl.textContent) : {};
  var root = (i18n.root || '/').replace(/\/?$/, '/');
  var dialog, state;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function build() {
    dialog = el('dialog', 'pp-qp');
    dialog.setAttribute('aria-label', '');
    var inner = el('div', 'pp-qp__inner');
    var close = el('button', 'pp-qp__close', '×');
    close.type = 'button';
    close.setAttribute('aria-label', i18n.close || 'Close');
    close.addEventListener('click', hide);
    var head = el('div', 'pp-qp__head');
    var img = el('img', 'pp-qp__img');
    img.alt = '';
    img.width = 96;
    img.height = 120;
    var info = el('div', 'pp-qp__info');
    var title = el('a', 'pp-qp__title');
    var price = el('div', 'pp-qp__price');
    info.append(title, price);
    head.append(img, info);
    var options = el('div', 'pp-qp__options');
    var error = el('p', 'pp-qp__error');
    error.hidden = true;
    var add = el('button', 'pp-qp__add');
    add.type = 'button';
    add.addEventListener('click', addToCart);
    options.addEventListener('change', onChange);
    inner.append(close, head, options, error, add);
    dialog.append(inner);
    // Click on the backdrop closes
    dialog.addEventListener('click', function (e) {
      if (e.target === dialog) hide();
    });
    document.body.append(dialog);
  }

  function hide() {
    if (dialog && dialog.open) dialog.close();
  }

  function findVariant(selected) {
    return state.data.variants.find(function (v) {
      return v[1].every(function (value, i) {
        return value === selected[i];
      });
    });
  }

  // Variant data is fetched on demand (product template "pp-data"), so cards stay light
  var cache = {};
  function loadData(card) {
    var dataEl = card.querySelector('[data-pp-card-data]');
    if (dataEl) return Promise.resolve(JSON.parse(dataEl.textContent));
    var url = card.dataset.ppUrl;
    if (!url) return Promise.reject(new Error('no product url'));
    if (!cache[url]) {
      cache[url] = fetch(url + (url.indexOf('?') < 0 ? '?' : '&') + 'view=pp-data', { headers: { Accept: 'text/html' } })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          return r.text();
        })
        .then(function (text) {
          return JSON.parse(text);
        })
        .catch(function (error) {
          delete cache[url];
          throw error;
        });
    }
    return cache[url];
  }

  function open(card) {
    var quick = card.querySelector('[data-pp-quick]');
    if (quick) quick.setAttribute('aria-busy', 'true');
    loadData(card)
      .then(function (data) {
        show(card, data);
      })
      .catch(function () {
        // Fall back to the product page
        var link = card.querySelector('[data-pp-card-link]');
        if (link) window.location.href = link.href;
      })
      .finally(function () {
        if (quick) quick.removeAttribute('aria-busy');
      });
  }

  function show(card, data) {
    if (!dialog) build();
    var start = Number(card.dataset.ppVariant || data.selected);
    var startVariant = data.variants.find(function (v) { return v[0] === start; }) ||
      data.variants.find(function (v) { return v[2]; }) || data.variants[0];
    var cardImg = card.querySelector('.pp-card__img:not(.pp-card__img--hover)');
    // Start with the photo the card already loaded, so the sheet shows it instantly
    state = { data: data, selected: startVariant[1].slice(), cardImg: cardImg && (cardImg.currentSrc || cardImg.src) };

    var title = dialog.querySelector('.pp-qp__title');
    title.textContent = data.title;
    title.href = data.url;
    dialog.setAttribute('aria-label', data.title);

    var options = dialog.querySelector('.pp-qp__options');
    options.textContent = '';
    // A single option with a single value (one variant) needs no picker
    if (!(data.variants.length === 1 && data.options.length === 1 && data.options[0].values.length <= 1)) {
      data.options.forEach(function (option, i) {
        var fieldset = el('fieldset', 'pp-qp__option');
        var legend = el('legend', 'pp-qp__legend');
        legend.append(option.name + ': ', el('span', 'pp-qp__chosen', option.values[state.selected[i]]));
        fieldset.append(legend);
        var list = el('div', 'pp-qp__values' + (i === data.colour ? ' pp-qp__values--colour' : ''));
        option.values.forEach(function (value, valueIndex) {
          var label = el('label', 'pp-qp__value');
          var input = el('input');
          input.type = 'radio';
          input.name = 'pp-qp-' + i;
          input.value = valueIndex;
          input.dataset.index = i;
          input.checked = valueIndex === state.selected[i];
          label.append(input);
          if (i === data.colour) {
            var thumb = el('img');
            thumb.src = data.images[valueIndex] || data.image;
            thumb.alt = value;
            thumb.width = 48;
            thumb.height = 60;
            thumb.loading = 'lazy';
            label.append(thumb);
            label.title = value;
          } else {
            label.append(el('span', '', value));
          }
          list.append(label);
        });
        fieldset.append(list);
        options.append(fieldset);
      });
    }

    dialog.querySelector('.pp-qp__error').hidden = true;
    update();
    dialog.showModal();
  }

  function onChange(e) {
    var input = e.target;
    if (!input.matches('input[type=radio]')) return;
    var optionIndex = Number(input.dataset.index);
    state.selected[optionIndex] = Number(input.value);
    input.closest('fieldset').querySelector('.pp-qp__chosen').textContent = state.data.options[optionIndex].values[Number(input.value)];
    dialog.querySelector('.pp-qp__error').hidden = true;
    update();
  }

  function update() {
    var data = state.data;
    var variant = findVariant(state.selected);
    state.variant = variant;

    // Grey out values that are sold out with the other current choices
    dialog.querySelectorAll('.pp-qp__value input').forEach(function (input) {
      var i = Number(input.dataset.index);
      var test = state.selected.slice();
      test[i] = Number(input.value);
      var match = findVariant(test);
      input.parentElement.classList.toggle('is-unavailable', !match || !match[2]);
    });

    var img = dialog.querySelector('.pp-qp__img');
    var colourValue = data.colour >= 0 ? state.selected[data.colour] : -1;
    var next = state.cardImg || (colourValue >= 0 && data.images[colourValue]) || data.image;
    state.cardImg = null;
    if (img.getAttribute('src') !== next) img.src = next;

    var price = dialog.querySelector('.pp-qp__price');
    price.textContent = '';
    var p = data.prices[variant ? variant[3] : 0];
    if (p) {
      price.append(el('span', 'pp-qp__now' + (p[1] ? ' pp-qp__now--sale' : ''), p[0]));
      if (p[1]) {
        price.append(el('s', 'pp-qp__was', p[1]), el('span', 'pp-qp__badge', '-' + p[2] + '%'));
      }
    }

    var add = dialog.querySelector('.pp-qp__add');
    add.disabled = !variant || !variant[2];
    add.textContent = !variant ? i18n.unavailable : variant[2] ? i18n.add : i18n.soldOut;
  }

  function addToCart() {
    var variant = state.variant;
    if (!variant || !variant[2]) return;
    var add = dialog.querySelector('.pp-qp__add');
    add.disabled = true;
    add.setAttribute('aria-busy', 'true');

    // Section ids of the theme cart (drawer), so the theme can redraw it
    var sections = [];
    document.querySelectorAll('cart-items-component[data-section-id]').forEach(function (el) {
      if (sections.indexOf(el.dataset.sectionId) < 0) sections.push(el.dataset.sectionId);
    });

    var themeEvents = import('@shopify/events').catch(function () { return null; });
    var deferred = null;
    themeEvents
      .then(function (ev) {
        if (!ev || !ev.CartLinesUpdateEvent) return;
        deferred = ev.CartLinesUpdateEvent.createPromise();
        // Sent from inside the sheet: the theme opens its drawer once the sheet has closed
        dialog.dispatchEvent(
          new ev.CartLinesUpdateEvent({
            action: 'add',
            context: 'product',
            lines: [{ merchandiseId: String(variant[0]), quantity: 1 }],
            promise: deferred.promise,
          })
        );
      })
      .then(function () {
        return fetch(root + 'cart/add.js', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ items: [{ id: variant[0], quantity: 1 }], sections: sections.join(',') }),
        });
      })
      .then(function (response) {
        return response.json().then(function (body) {
          if (!response.ok) throw new Error(body.description || body.message || i18n.error);
          return body;
        });
      })
      .then(function (added) {
        hide();
        if (!deferred) {
          window.location.href = i18n.cartUrl || '/cart';
          return;
        }
        return themeEvents.then(function (ev) {
          return fetch(root + 'cart.js', { headers: { Accept: 'application/json' } })
            .then(function (r) { return r.json(); })
            .then(function (cart) {
              deferred.resolve({
                cart: ev.CartLinesUpdateEvent.createCartFromAjaxResponse(cart),
                detail: { items: cart.items, source: 'pp-quick-pick', itemCount: 1, sections: added.sections, didError: false },
              });
            });
        });
      })
      .catch(function (error) {
        if (deferred) deferred.reject(error);
        var box = dialog.querySelector('.pp-qp__error');
        box.textContent = error.message || i18n.error;
        box.hidden = false;
      })
      .finally(function () {
        add.removeAttribute('aria-busy');
        update();
      });
  }

  // Card behaviour (delegated, so it works for every card on the page)
  document.addEventListener('click', function (e) {
    var quick = e.target.closest('[data-pp-quick]');
    if (quick) {
      e.preventDefault();
      open(quick.closest('[data-pp-card]'));
      return;
    }

    var swatch = e.target.closest('[data-pp-swatch]');
    if (swatch) {
      e.preventDefault();
      var card = swatch.closest('[data-pp-card]');
      card.querySelectorAll('[data-pp-swatch]').forEach(function (s) {
        s.classList.toggle('is-active', s === swatch);
      });
      var img = card.querySelector('.pp-card__img:not(.pp-card__img--hover)');
      if (img && swatch.dataset.img) {
        img.removeAttribute('srcset');
        img.src = swatch.dataset.img;
      }
      card.dataset.ppVariant = swatch.dataset.variant;
      card.querySelectorAll('[data-pp-card-link]').forEach(function (a) {
        var url = new URL(a.href, location.href);
        url.searchParams.set('variant', swatch.dataset.variant);
        a.href = url.pathname + url.search;
      });
      return;
    }

    var arrow = e.target.closest('[data-pp-row-arrow]');
    if (arrow) {
      var track = arrow.closest('[data-pp-row]').querySelector('.pp-row__track');
      track.scrollBy({ left: Number(arrow.dataset.dir) * track.clientWidth * 0.9, behavior: 'smooth' });
      return;
    }

    if (e.target.closest('[data-pp-tab]')) requestAnimationFrame(updateArrows);
  });

  // Start loading the variant data as soon as the shopper reaches for "Choose"
  ['pointerdown', 'focusin'].forEach(function (type) {
    document.addEventListener(
      type,
      function (e) {
        var quick = e.target.closest && e.target.closest('[data-pp-quick]');
        if (quick) loadData(quick.closest('[data-pp-card]')).catch(function () {});
      },
      { passive: true }
    );
  });

  // Second image on hover: only loaded when a mouse is on the card
  document.addEventListener('pointerover', function (e) {
    if (e.pointerType !== 'mouse') return;
    var card = e.target.closest && e.target.closest('[data-pp-card]');
    var hover = card && card.querySelector('.pp-card__img--hover[data-srcset]');
    if (!hover) return;
    hover.srcset = hover.dataset.srcset;
    hover.removeAttribute('data-srcset');
  });

  function updateArrows() {
    document.querySelectorAll('[data-pp-row]').forEach(function (row) {
      var track = row.querySelector('.pp-row__track');
      var max = track.scrollWidth - track.clientWidth - 2;
      row.querySelectorAll('[data-pp-row-arrow]').forEach(function (a) {
        a.disabled = a.dataset.dir === '-1' ? track.scrollLeft <= 2 : track.scrollLeft >= max;
      });
    });
  }

  document.addEventListener(
    'scroll',
    function (e) {
      if (e.target.classList && e.target.classList.contains('pp-row__track')) updateArrows();
    },
    { capture: true, passive: true }
  );
  window.addEventListener('resize', updateArrows, { passive: true });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', updateArrows);
  else updateArrows();
})();
