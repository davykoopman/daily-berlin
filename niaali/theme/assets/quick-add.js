import { morph } from '@theme/morph';
import { Component } from '@theme/component';
import { CartUpdateEvent, ThemeEvents, VariantSelectedEvent } from '@theme/events';
import { DialogComponent, DialogCloseEvent } from '@theme/dialog';
import { mediaQueryLarge, isMobileBreakpoint, getIOSVersion } from '@theme/utilities';
import VariantPicker from '@theme/variant-picker';

/**
 * Speed-ups (Niaali): the quick add content is loaded from the product section only
 * (Section Rendering API, ~6x smaller than the full page), fetched ahead on intent
 * (hover on desktop, touch on mobile) and shared by every quick add button on the page.
 * The section id (template--<id>__<section>) differs per store, so it is learned from
 * the first full product page of the visit and remembered for the session.
 */
const SECTION_ID_KEY = 'quick-add-section-id';
/** @type {Map<string, Element>} */
const sharedContent = new Map();
/** @type {Map<string, Promise<Element | null>>} */
const pendingContent = new Map();

/** @param {string} key */
function readSessionValue(key) {
  try {
    return sessionStorage.getItem(key);
  } catch (error) {
    return null;
  }
}

/**
 * @param {string} key
 * @param {string} value
 */
function writeSessionValue(key, value) {
  try {
    sessionStorage.setItem(key, value);
  } catch (error) {
    // Storage unavailable (private mode): the full page is used instead
  }
}

export class QuickAddComponent extends Component {
  /** @type {AbortController | null} */
  #abortController = null;
  /** @type {AbortController} */
  #cartUpdateAbortController = new AbortController();
  /** @type {AbortController | null} */
  #intentAbortController = null;
  /** @type {number | undefined} */
  #intentTimer;

  get productPageUrl() {
    const productCard = /** @type {import('./product-card').ProductCard | null} */ (this.closest('product-card'));
    const hotspotProduct = /** @type {import('./product-hotspot').ProductHotspotComponent | null} */ (
      this.closest('product-hotspot-component')
    );
    const productLink = productCard?.getProductCardLink() || hotspotProduct?.getHotspotProductLink();

    if (!productLink?.href) return '';

    const url = new URL(productLink.href);

    if (url.searchParams.has('variant')) {
      return url.toString();
    }

    const selectedVariantId = this.#getSelectedVariantId();
    if (selectedVariantId) {
      url.searchParams.set('variant', selectedVariantId);
    }

    return url.toString();
  }

  /**
   * Gets the currently selected variant ID from the product card
   * @returns {string | null} The variant ID or null
   */
  #getSelectedVariantId() {
    const productCard = /** @type {import('./product-card').ProductCard | null} */ (this.closest('product-card'));
    return productCard?.getSelectedVariantId() || null;
  }

  connectedCallback() {
    super.connectedCallback();

    mediaQueryLarge.addEventListener('change', this.#closeQuickAddModal);
    document.addEventListener(ThemeEvents.cartUpdate, this.#handleCartUpdate, {
      signal: this.#cartUpdateAbortController.signal,
    });
    document.addEventListener(ThemeEvents.variantSelected, this.#updateQuickAddButtonState.bind(this));

    // Load the product as soon as the shopper shows intent, so the modal opens instantly
    this.#intentAbortController = new AbortController();
    const { signal } = this.#intentAbortController;
    const card = this.closest('product-card') || this.closest('product-hotspot-component');
    card?.addEventListener('pointerenter', this.#handleIntent, { signal });
    card?.addEventListener('pointerleave', this.#cancelIntent, { signal });
    this.addEventListener('touchstart', this.#handleIntent, { passive: true, signal });
    this.addEventListener('focusin', this.#handleIntent, { signal });
  }

  disconnectedCallback() {
    this.#intentAbortController?.abort();
    this.#cancelIntent();
    super.disconnectedCallback();

    mediaQueryLarge.removeEventListener('change', this.#closeQuickAddModal);
    this.#abortController?.abort();
    this.#cartUpdateAbortController.abort();
    document.removeEventListener(ThemeEvents.variantSelected, this.#updateQuickAddButtonState.bind(this));
  }

  /**
   * Clears the cached content when cart is updated
   */
  #handleCartUpdate = () => {
    sharedContent.clear();
  };

  /**
   * Starts loading the product when the shopper hovers the card, touches or focuses the button
   * @param {Event} event
   */
  #handleIntent = (event) => {
    if (event instanceof PointerEvent && event.type === 'pointerenter' && event.pointerType !== 'mouse') return;
    if (this.dataset.quickAddButton !== 'choose') return;

    clearTimeout(this.#intentTimer);
    // A short delay on hover, so moving the mouse across a row does not load every product
    const delay = event.type === 'pointerenter' ? 120 : 0;
    this.#intentTimer = window.setTimeout(() => this.#loadProductGrid(this.productPageUrl), delay);
  };

  #cancelIntent = () => {
    clearTimeout(this.#intentTimer);
  };

  /**
   * Loads the product grid once per URL; parallel calls share the same request
   * @param {string} url - Product page URL
   * @returns {Promise<Element | null>}
   */
  #loadProductGrid(url) {
    if (!url) return Promise.resolve(null);

    const cached = sharedContent.get(url);
    if (cached) return Promise.resolve(cached);

    let pending = pendingContent.get(url);
    if (!pending) {
      pending = this.#fetchProductGrid(url)
        .then((grid) => {
          if (grid) sharedContent.set(url, grid);
          return grid;
        })
        .catch(() => null)
        .finally(() => pendingContent.delete(url));
      pendingContent.set(url, pending);
    }

    return pending;
  }

  /**
   * Fetches only the product section; falls back to the full page (e.g. a product on another template)
   * @param {string} url - Product page URL
   * @returns {Promise<Element | null>}
   */
  async #fetchProductGrid(url) {
    const sectionId = readSessionValue(SECTION_ID_KEY);

    if (sectionId) {
      const sectionUrl = new URL(url);
      sectionUrl.searchParams.set('section_id', sectionId);

      const html = await this.#fetchDocument(sectionUrl.toString()).catch(() => null);
      const grid = html?.querySelector('[data-product-grid-content]');

      // Only use it when it is the full product form (a product on another template renders differently)
      if (grid?.querySelector('product-form-component')) return /** @type {Element} */ (grid.cloneNode(true));
    }

    const html = await this.#fetchDocument(url);
    const grid = html?.querySelector('[data-product-grid-content]');
    if (!grid) return null;

    const section = grid.closest('.shopify-section');
    if (section?.id.startsWith('shopify-section-')) {
      writeSessionValue(SECTION_ID_KEY, section.id.replace('shopify-section-', ''));
    }

    // Cache a clone to avoid modifying the original
    return /** @type {Element} */ (grid.cloneNode(true));
  }

  /**
   * Fetches and parses a page without aborting other requests (used for loading ahead)
   * @param {string} url
   * @returns {Promise<Document | null>}
   */
  async #fetchDocument(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Failed to fetch product page: HTTP error ${response.status}`);
    return new DOMParser().parseFromString(await response.text(), 'text/html');
  }

  /**
   * Re-renders the variant picker in the quick-add modal.
   * @param {Element} newHtml - The element to re-render.
   */
  #updateVariantPicker(newHtml) {
    const modalContent = document.getElementById('quick-add-modal-content');
    if (!modalContent) return;
    const variantPicker = /** @type {VariantPicker | null} */ (modalContent.querySelector('variant-picker'));
    variantPicker?.updateVariantPicker(newHtml);
  }

  /**
   * Handles quick add button click
   * @param {Event} event - The click event
   */
  handleClick = async (event) => {
    event.preventDefault();

    const currentUrl = this.productPageUrl;
    const button = event.target instanceof Element ? event.target.closest('button') : null;

    // Instant feedback while the product loads (only shown when it is not loaded yet)
    if (!sharedContent.has(currentUrl)) button?.setAttribute('aria-busy', 'true');

    const productGrid = await this.#loadProductGrid(currentUrl);

    button?.removeAttribute('aria-busy');

    if (!productGrid) {
      // Never leave the shopper with an empty modal: go to the product page instead
      if (currentUrl) window.location.href = currentUrl;
      return;
    }

    // Use a fresh clone from the cache
    const freshContent = /** @type {Element} */ (productGrid.cloneNode(true));
    await this.updateQuickAddModal(freshContent);
    this.#updateVariantPicker(productGrid);

    this.#openQuickAddModal();
  };

  #resetScroll() {
    const dialogComponent = document.getElementById('quick-add-dialog');
    if (!(dialogComponent instanceof QuickAddDialog)) return;

    const productDetails = dialogComponent.querySelector('.product-details');
    const productMedia = dialogComponent.querySelector('.product-information__media');
    productDetails?.scrollTo({ top: 0, behavior: 'instant' });
    productMedia?.scrollTo({ top: 0, behavior: 'instant' });
  }

  /** @param {QuickAddDialog} dialogComponent */
  #stayVisibleUntilDialogCloses(dialogComponent) {
    this.toggleAttribute('stay-visible', true);

    dialogComponent.addEventListener(DialogCloseEvent.eventName, () => this.toggleAttribute('stay-visible', false), {
      once: true,
    });
  }

  #openQuickAddModal = () => {
    const dialogComponent = document.getElementById('quick-add-dialog');
    if (!(dialogComponent instanceof QuickAddDialog)) return;

    this.#stayVisibleUntilDialogCloses(dialogComponent);

    dialogComponent.showDialog();

    // is nondeterministic when the open attribute is set on the dialog element after .showDialog() is called.
    // Waiting until the open animation starts seemed to be the most reliable metric here.
    const dialog = dialogComponent.refs?.dialog;
    if (!dialog) return;
    dialog.addEventListener('animationstart', this.#resetScroll.bind(this), { once: true });
  };

  #closeQuickAddModal = () => {
    const dialogComponent = document.getElementById('quick-add-dialog');
    if (!(dialogComponent instanceof QuickAddDialog)) return;

    dialogComponent.closeDialog();
  };

  /**
   * Fetches the product page content
   * @param {string} productPageUrl - The URL of the product page to fetch
   * @returns {Promise<Document | null>}
   */
  async fetchProductPage(productPageUrl) {
    if (!productPageUrl) return null;

    // We use this to abort the previous fetch request if it's still pending.
    this.#abortController?.abort();
    this.#abortController = new AbortController();

    try {
      const response = await fetch(productPageUrl, {
        signal: this.#abortController.signal,
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch product page: HTTP error ${response.status}`);
      }

      const responseText = await response.text();
      const html = new DOMParser().parseFromString(responseText, 'text/html');

      return html;
    } catch (error) {
      if (error.name === 'AbortError') {
        return null;
      } else {
        throw error;
      }
    } finally {
      this.#abortController = null;
    }
  }

  /**
   * Re-renders the variant picker.
   * @param {Element} productGrid - The product grid element
   */
  async updateQuickAddModal(productGrid) {
    const modalContent = document.getElementById('quick-add-modal-content');

    if (!productGrid || !modalContent) return;

    if (isMobileBreakpoint()) {
      const productDetails = productGrid.querySelector('.product-details');
      const productFormComponent = productGrid.querySelector('product-form-component');
      const variantPicker = productGrid.querySelector('variant-picker');
      const productPrice = productGrid.querySelector('product-price');
      const productTitle = document.createElement('a');
      productTitle.textContent = this.dataset.productTitle || '';

      // Make product title as a link to the product page
      productTitle.href = this.productPageUrl;

      const productHeader = document.createElement('div');
      productHeader.classList.add('product-header');

      productHeader.appendChild(productTitle);
      if (productPrice) {
        productHeader.appendChild(productPrice);
      }
      productGrid.appendChild(productHeader);

      if (variantPicker) {
        productGrid.appendChild(variantPicker);
      }
      if (productFormComponent) {
        productGrid.appendChild(productFormComponent);
      }

      productDetails?.remove();
    }

    morph(modalContent, productGrid);

    this.#syncVariantSelection(modalContent);
  }

  /**
   * Updates the quick-add button state based on whether a swatch is selected
   * @param {VariantSelectedEvent} event - The variant selected event
   */
  #updateQuickAddButtonState(event) {
    if (!(event.target instanceof HTMLElement)) return;
    if (event.target.closest('product-card') !== this.closest('product-card')) return;
    const productOptionsCount = this.dataset.productOptionsCount;
    const quickAddButton = productOptionsCount === '1' ? 'add' : 'choose';
    this.setAttribute('data-quick-add-button', quickAddButton);
  }

  /**
   * Syncs the variant selection from the product card to the modal
   * @param {Element} modalContent - The modal content element
   */
  #syncVariantSelection(modalContent) {
    const selectedVariantId = this.#getSelectedVariantId();
    if (!selectedVariantId) return;

    // Find and check the corresponding input in the modal
    const modalInputs = modalContent.querySelectorAll('input[type="radio"][data-variant-id]');
    for (const input of modalInputs) {
      if (input instanceof HTMLInputElement && input.dataset.variantId === selectedVariantId && !input.checked) {
        input.checked = true;
        input.dispatchEvent(new Event('change', { bubbles: true }));
        break;
      }
    }
  }
}

if (!customElements.get('quick-add-component')) {
  customElements.define('quick-add-component', QuickAddComponent);
}

class QuickAddDialog extends DialogComponent {
  #abortController = new AbortController();

  connectedCallback() {
    super.connectedCallback();

    this.addEventListener(ThemeEvents.cartUpdate, this.handleCartUpdate, { signal: this.#abortController.signal });
    this.addEventListener(ThemeEvents.variantUpdate, this.#updateProductTitleLink);

    this.addEventListener(DialogCloseEvent.eventName, this.#handleDialogClose);
  }

  disconnectedCallback() {
    super.disconnectedCallback();

    this.#abortController.abort();
    this.removeEventListener(DialogCloseEvent.eventName, this.#handleDialogClose);
  }

  /**
   * Closes the dialog
   * @param {CartUpdateEvent} event - The cart update event
   */
  handleCartUpdate = (event) => {
    if (event.detail.data.didError) return;
    this.closeDialog();
  };

  #updateProductTitleLink = (/** @type {CustomEvent} */ event) => {
    const anchorElement = /** @type {HTMLAnchorElement} */ (
      event.detail.data.html?.querySelector('.view-product-title a')
    );
    const viewMoreDetailsLink = /** @type {HTMLAnchorElement} */ (this.querySelector('.view-product-title a'));
    const mobileProductTitle = /** @type {HTMLAnchorElement} */ (this.querySelector('.product-header a'));

    if (!anchorElement) return;

    if (viewMoreDetailsLink) viewMoreDetailsLink.href = anchorElement.href;
    if (mobileProductTitle) mobileProductTitle.href = anchorElement.href;
  };

  #handleDialogClose = () => {
    const iosVersion = getIOSVersion();
    /**
     * This is a patch to solve an issue with the UI freezing when the dialog is closed.
     * To reproduce it, use iOS 16.0.
     */
    if (!iosVersion || iosVersion.major >= 17 || (iosVersion.major === 16 && iosVersion.minor >= 4)) return;

    requestAnimationFrame(() => {
      /** @type {HTMLElement | null} */
      const grid = document.querySelector('#ResultsList [product-grid-view]');
      if (grid) {
        const currentWidth = grid.getBoundingClientRect().width;
        grid.style.width = `${currentWidth - 1}px`;
        requestAnimationFrame(() => {
          grid.style.width = '';
        });
      }
    });
  };
}

if (!customElements.get('quick-add-dialog')) {
  customElements.define('quick-add-dialog', QuickAddDialog);
}
