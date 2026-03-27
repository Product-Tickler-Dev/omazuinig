# Oma Zuinig Interactive Prototype — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:executing-plans to implement this plan task-by-task.

**Goal:** Build a high-fidelity interactive HTML/CSS/JS prototype of the Oma Zuinig grocery price comparison app — 5 screens with navigation, mock data, Oma personality, and the full visual design system. Mobile-first, runs in any browser.

**Architecture:** Single `index.html` file with embedded CSS and vanilla JS. No build tools, no framework. Screens are `<section>` elements toggled by JS. Mock data is a JS object. Google Fonts loaded via CDN (Inter + Caveat). Mascot images referenced from the project folder.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, flexbox, animations), vanilla JavaScript (ES6+), Google Fonts CDN.

---

### Task 0: Project Setup & Base HTML Shell

**Files:**
- Create: `prototype/index.html`

**Step 1: Create the prototype directory**

```bash
mkdir -p /c/omazuinig/prototype
```

**Step 2: Write the base HTML shell**

Create `prototype/index.html` with:
- HTML5 doctype, `<meta charset>`, `<meta viewport>` for mobile
- Google Fonts link: Inter (400, 700) + Caveat (400)
- CSS custom properties for the full color palette:
  - `--orange: #FF6200`
  - `--green: #00C853`
  - `--blue: #0052CC`
  - `--cream: #FFF9F0`
  - `--red: #E6392E`
  - `--dark: #1C1C1C`
- CSS reset (box-sizing, margin, padding)
- Body styled: `font-family: 'Inter', sans-serif; background: var(--cream); color: var(--dark);`
- Typography classes: `.heading` (Inter Bold), `.oma-speech` (Caveat)
- `<div id="app">` wrapper
- 5 `<section>` elements with IDs: `screen-home`, `screen-lijst`, `screen-vergelijk`, `screen-deals`, `screen-oma` — all hidden except home
- Bottom nav bar: 5 buttons with emoji icons and Dutch labels (Home, Lijst, Vergelijk, Deals, Mijn Oma)
- JS: navigation function that shows/hides sections on tab click, updates active tab styling
- Bottom nav is fixed to bottom, 60px tall, white background, subtle top shadow

**Step 3: Verify in browser**

Open `prototype/index.html` in browser. Should see:
- Cream background
- Bottom nav with 5 tabs
- Clicking tabs switches between empty sections
- Mobile-width (375px) layout

**Step 4: Commit**

```bash
cd /c/omazuinig && git init && git add prototype/index.html && git commit -m "feat: base HTML shell with navigation and design system"
```

---

### Task 1: Mock Data Layer

**Files:**
- Modify: `prototype/index.html` (add `<script>` block before closing `</body>`)

**Step 1: Add mock data object**

Add a `<script>` section with a `DATA` object containing:

**Stores array:**
```js
const STORES = [
  { id: 'ah', name: 'Albert Heijn', short: 'AH', color: '#00A0E2' },
  { id: 'jumbo', name: 'Jumbo', short: 'Jumbo', color: '#FFD700' },
  { id: 'lidl', name: 'Lidl', short: 'Lidl', color: '#0050AA' },
  { id: 'aldi', name: 'Aldi', short: 'Aldi', color: '#00599C' },
  { id: 'plus', name: 'Plus', short: 'Plus', color: '#E3000B' },
  { id: 'dirk', name: 'Dirk', short: 'Dirk', color: '#E31937' }
];
```

**Products array** (10 items with realistic Dutch prices per store):
```js
const PRODUCTS = [
  {
    id: 1, name: 'Halfvolle melk', brand: 'Huismerk', size: '1L',
    category: 'zuivel', unit: 'L', img: '🥛',
    prices: { ah: 1.29, jumbo: 1.25, lidl: 0.99, aldi: 0.95, plus: 1.19, dirk: 1.09 }
  },
  {
    id: 2, name: 'Gouda kaas jong belegen', brand: 'Huismerk', size: '500g',
    category: 'zuivel', unit: 'kg', img: '🧀',
    prices: { ah: 4.99, jumbo: 4.79, lidl: 3.99, aldi: 3.89, plus: 4.49, dirk: 4.29 }
  },
  {
    id: 3, name: 'Volkoren brood', brand: 'Huismerk', size: '800g',
    category: 'brood', unit: 'kg', img: '🍞',
    prices: { ah: 1.89, jumbo: 1.79, lidl: 1.49, aldi: 1.39, plus: 1.69, dirk: 1.59 }
  },
  {
    id: 4, name: 'Scharreleieren', brand: 'Huismerk', size: '10 stuks',
    category: 'zuivel', unit: 'stuk', img: '🥚',
    prices: { ah: 3.29, jumbo: 2.99, lidl: 2.69, aldi: 2.59, plus: 2.89, dirk: 2.79 }
  },
  {
    id: 5, name: 'Heineken Pilsener', brand: 'Heineken', size: '6-pack',
    category: 'dranken', unit: 'pack', img: '🍺',
    prices: { ah: 5.99, jumbo: 5.49, lidl: 5.29, aldi: 5.19, plus: 5.69, dirk: 5.39 }
  },
  {
    id: 6, name: 'Aroma Rood koffie', brand: 'Douwe Egberts', size: '500g',
    category: 'dranken', unit: 'kg', img: '☕',
    prices: { ah: 6.99, jumbo: 6.49, lidl: 5.99, aldi: 5.79, plus: 6.29, dirk: 6.19 }
  },
  {
    id: 7, name: 'Pindakaas', brand: 'Calvé', size: '650g',
    category: 'brood', unit: 'kg', img: '🥜',
    prices: { ah: 4.49, jumbo: 3.99, lidl: 3.79, aldi: 3.69, plus: 4.19, dirk: 3.89 }
  },
  {
    id: 8, name: 'Paprika rood', brand: '', size: 'per stuk',
    category: 'groente', unit: 'stuk', img: '🫑',
    prices: { ah: 1.19, jumbo: 0.99, lidl: 0.89, aldi: 0.85, plus: 0.99, dirk: 0.95 }
  },
  {
    id: 9, name: 'Melkchocolade hagelslag', brand: 'De Ruijter', size: '400g',
    category: 'brood', unit: 'kg', img: '🍫',
    prices: { ah: 2.99, jumbo: 2.79, lidl: 2.49, aldi: 2.39, plus: 2.69, dirk: 2.59 }
  },
  {
    id: 10, name: 'Karnemelk', brand: 'Huismerk', size: '1L',
    category: 'zuivel', unit: 'L', img: '🥛',
    prices: { ah: 1.09, jumbo: 0.99, lidl: 0.89, aldi: 0.85, plus: 0.99, dirk: 0.95 }
  }
];
```

**Weekly deals array** (subset of products with discount info):
```js
const DEALS = [
  { productId: 5, store: 'ah', oldPrice: 5.99, newPrice: 3.99, discount: 33 },
  { productId: 6, store: 'jumbo', oldPrice: 6.49, newPrice: 4.49, discount: 31 },
  { productId: 7, store: 'lidl', oldPrice: 3.79, newPrice: 1.99, discount: 47 },
  { productId: 2, store: 'aldi', oldPrice: 3.89, newPrice: 2.49, discount: 36 },
  { productId: 9, store: 'dirk', oldPrice: 2.59, newPrice: 1.49, discount: 42 },
  { productId: 4, store: 'plus', oldPrice: 2.89, newPrice: 1.79, discount: 38 },
  { productId: 3, store: 'ah', oldPrice: 1.89, newPrice: 0.99, discount: 48 },
  { productId: 8, store: 'jumbo', oldPrice: 0.99, newPrice: 0.59, discount: 40 }
];
```

**Shopping list state:**
```js
let shoppingList = [
  { productId: 1, checked: false },
  { productId: 2, checked: false },
  { productId: 4, checked: false },
  { productId: 7, checked: false },
  { productId: 6, checked: true }
];
let optimizeMode = 'single'; // 'single' or 'split'
```

**Helper functions:**
```js
function getProduct(id) { return PRODUCTS.find(p => p.id === id); }
function getStore(id) { return STORES.find(s => s.id === id); }
function getCheapestStore(product) {
  return Object.entries(product.prices)
    .sort((a, b) => a[1] - b[1])[0];
}
function getMostExpensiveStore(product) {
  return Object.entries(product.prices)
    .sort((a, b) => b[1] - a[1])[0];
}
function formatPrice(n) { return '€' + n.toFixed(2).replace('.', ','); }
```

**Step 2: Commit**

```bash
git add prototype/index.html && git commit -m "feat: add mock data layer with Dutch grocery products and helpers"
```

---

### Task 2: Shared UI Components (CSS + JS)

**Files:**
- Modify: `prototype/index.html` (CSS section + JS section)

**Step 1: Add reusable CSS component styles**

Add to the `<style>` block:

- **Store badge**: `.store-badge` — small pill (border-radius: 12px, padding: 2px 8px, font-size: 12px, white text on store color). `.store-badge.cheapest` gets green background + slight scale. `.store-badge.duur` gets red background + strikethrough.
- **Deal card**: `.deal-card` — white background, border-radius: 16px, box-shadow, padding: 16px. Contains: emoji/img, product name, store logo, prices, discount badge.
- **Oma speech bubble**: `.oma-bubble` — cream background (#FFF9F0), border: 2px solid var(--orange), border-radius: 16px 16px 16px 4px, padding: 12px 16px, font-family: 'Caveat', font-size: 18px, max-width: 280px. Small Oma avatar (32px circle) floated left.
- **Discount badge**: `.discount-badge` — orange circle with white text, `-XX%`.
- **Hamsteralert badge**: `.hamster-badge` — orange pill, bold text, "Hamsteralert!".
- **Beste Keuze stamp**: `.beste-keuze` — green border, green text, checkmark icon.
- **Category pills**: `.category-pill` — border-radius: 20px, border: 1.5px solid var(--blue), padding: 4px 14px, cursor: pointer. `.category-pill.active` — filled blue background, white text.
- **Header bar**: `.top-bar` — height: 56px, white background, centered logo text "Oma Zuinig" in orange bold, small winking emoji.
- **Screen container**: `.screen` — padding: 16px 16px 80px (space for bottom nav), hidden by default, `.screen.active` shows.
- **Animations**:
  - `@keyframes slideUp` — translateY(20px) → 0, opacity 0 → 1 (200ms)
  - `@keyframes confetti` — scale(0) → scale(1) with rotate (300ms)
  - `@keyframes fadeIn` — opacity 0 → 1 (200ms)
  - `.animate-in` class applies slideUp

**Step 2: Add reusable JS render functions**

```js
function renderStoreBadge(storeId, price, cheapest = false, duur = false) {
  const store = getStore(storeId);
  const classes = ['store-badge', cheapest ? 'cheapest' : '', duur ? 'duur' : ''].filter(Boolean).join(' ');
  return `<span class="${classes}" style="background:${cheapest ? 'var(--green)' : duur ? 'var(--red)' : store.color}">${store.short} ${formatPrice(price)}</span>`;
}

function renderOmaBubble(text) {
  return `<div class="oma-bubble animate-in"><span class="oma-avatar">👵</span> ${text}</div>`;
}

function renderDealCard(deal) {
  const product = getProduct(deal.productId);
  const store = getStore(deal.store);
  const isHamster = deal.discount >= 40;
  return `
    <div class="deal-card animate-in">
      <div class="deal-card__emoji">${product.img}</div>
      <div class="deal-card__store" style="color:${store.color}">${store.short}</div>
      ${isHamster ? '<span class="hamster-badge">Hamsteralert!</span>' : ''}
      <div class="deal-card__name">${product.name}</div>
      <div class="deal-card__size">${product.brand ? product.brand + ' · ' : ''}${product.size}</div>
      <div class="deal-card__prices">
        <span class="price-old">${formatPrice(deal.oldPrice)}</span>
        <span class="price-new">${formatPrice(deal.newPrice)}</span>
      </div>
      <span class="discount-badge">-${deal.discount}%</span>
    </div>`;
}

function renderProductCard(product) {
  const [cheapestId] = getCheapestStore(product);
  const [duurId] = getMostExpensiveStore(product);
  const badges = Object.entries(product.prices)
    .sort((a, b) => a[1] - b[1])
    .map(([sid, price]) => renderStoreBadge(sid, price, sid === cheapestId, sid === duurId))
    .join('');
  return `
    <div class="product-card animate-in">
      <div class="product-card__left">
        <span class="product-card__emoji">${product.img}</span>
      </div>
      <div class="product-card__right">
        <div class="product-card__name">${product.name}</div>
        <div class="product-card__meta">${product.brand ? product.brand + ' · ' : ''}${product.size}</div>
        <div class="product-card__badges">${badges}</div>
      </div>
      <div class="product-card__action">
        <button class="btn-add" onclick="addToList(${product.id})">+ Lijst</button>
      </div>
    </div>`;
}
```

**Step 3: Commit**

```bash
git add prototype/index.html && git commit -m "feat: add shared UI components — badges, cards, bubbles, animations"
```

---

### Task 3: Home Screen

**Files:**
- Modify: `prototype/index.html` (fill `#screen-home` section + add render function)

**Step 1: Build the Home screen HTML structure**

Inside `#screen-home`:
- Top bar with "Oma Zuinig" logo text (orange, bold) + 👵 winking emoji
- Hero banner: orange gradient (linear-gradient 135deg, #FF6200 → #FF8A3D), white text, Oma greeting: "Hoi lieverd! Oma heeft vandaag €14,20 voor je bespaard!", rounded corners (20px), padding 24px
- Quick actions: 3 equal cards in a CSS grid (1fr 1fr 1fr), each with emoji icon + label. Cards: "🛒 Mijn Lijst" (navigates to lijst), "🔍 Vergelijk" (navigates to vergelijk), "📷 Scan" (shows "Binnenkort!" toast). White cards, rounded, shadow, clickable.
- Section heading: "Vandaag in de aanbieding" with a small Oma bubble: "Dit wil je niet missen!"
- Horizontal scrolling deal cards row: `display: flex; overflow-x: auto; gap: 12px; scroll-snap-type: x mandatory;` — render top 5 deals using `renderDealCard()`

**Step 2: Add JS render function**

```js
function renderHome() {
  const dealsHtml = DEALS.slice(0, 5).map(d => renderDealCard(d)).join('');
  document.getElementById('screen-home').innerHTML = `
    <div class="top-bar">👵 <span class="logo">Oma Zuinig</span></div>
    <div class="hero-banner">
      <p class="hero-greeting">Hoi lieverd!</p>
      <p class="hero-savings">Oma heeft vandaag <strong>€14,20</strong> voor je bespaard!</p>
    </div>
    <div class="quick-actions">
      <div class="quick-card" onclick="navigate('lijst')">🛒<br>Mijn Lijst</div>
      <div class="quick-card" onclick="navigate('vergelijk')">🔍<br>Vergelijk</div>
      <div class="quick-card" onclick="showToast('Binnenkort beschikbaar!')">📷<br>Scan</div>
    </div>
    <div class="section-header">
      <h2>Vandaag in de aanbieding</h2>
      ${renderOmaBubble('Dit wil je niet missen!')}
    </div>
    <div class="deals-scroll">${dealsHtml}</div>
  `;
}
```

Call `renderHome()` on page load.

**Step 3: Verify**

Open in browser. Should see: orange hero banner with greeting, 3 quick-action cards, scrollable deals row. Clicking "Mijn Lijst" or "Vergelijk" navigates.

**Step 4: Commit**

```bash
git add prototype/index.html && git commit -m "feat: home screen with hero banner, quick actions, and deals carousel"
```

---

### Task 4: Mijn Lijst Screen

**Files:**
- Modify: `prototype/index.html` (fill `#screen-lijst` + add render/interaction functions)

**Step 1: Build the Lijst screen**

Inside `#screen-lijst`:
- Top bar: "Mijn Boodschappenlijst" + item count badge
- Add-item input: styled search bar with placeholder "Voeg product toe...", dropdown autocomplete from PRODUCTS on keyup (filter by name, show max 5 matches). Clicking a match calls `addToList(id)`.
- List items: each item is a row with:
  - Checkbox (toggles `checked` state, strikes through item)
  - Product emoji + name + size
  - Row of store badges (sorted cheapest first, cheapest = green)
  - Checked items move to bottom, grayed out
- Sticky footer (position: sticky, bottom: 60px — above nav):
  - "Oma's Advies" section
  - Toggle: two buttons "1 Winkel" / "Slim splitsen"
  - If "1 Winkel": show cheapest single-store total: "Alles bij [store]: €XX,XX"
  - If "Slim splitsen": show optimized total: "Lidl + AH = €XX,XX — besparing €X,XX!"
  - Small Oma avatar + speech bubble with the advice

**Step 2: Add JS functions**

```js
function addToList(productId) {
  if (!shoppingList.find(i => i.productId === productId)) {
    shoppingList.push({ productId, checked: false });
    renderLijst();
    showOmaBubble('Slim bezig, lieverd!');
  }
}

function toggleItem(productId) {
  const item = shoppingList.find(i => i.productId === productId);
  if (item) { item.checked = !item.checked; renderLijst(); }
}

function removeFromList(productId) {
  shoppingList = shoppingList.filter(i => i.productId !== productId);
  renderLijst();
}

function calculateBestStore() {
  const unchecked = shoppingList.filter(i => !i.checked);
  const storeTotals = {};
  STORES.forEach(s => { storeTotals[s.id] = 0; });
  unchecked.forEach(item => {
    const product = getProduct(item.productId);
    STORES.forEach(s => { storeTotals[s.id] += product.prices[s.id]; });
  });
  return Object.entries(storeTotals).sort((a, b) => a[1] - b[1]);
}

function calculateSplitSavings() {
  const unchecked = shoppingList.filter(i => !i.checked);
  let splitTotal = 0;
  const storesUsed = new Set();
  unchecked.forEach(item => {
    const product = getProduct(item.productId);
    const [cheapestId, cheapestPrice] = getCheapestStore(product);
    splitTotal += cheapestPrice;
    storesUsed.add(cheapestId);
  });
  const [bestStoreId, bestStoreTotal] = calculateBestStore()[0];
  return {
    splitTotal,
    storesUsed: [...storesUsed],
    singleStore: bestStoreId,
    singleTotal: bestStoreTotal,
    savings: bestStoreTotal - splitTotal
  };
}

function renderLijst() {
  const unchecked = shoppingList.filter(i => !i.checked);
  const checked = shoppingList.filter(i => i.checked);
  const sorted = [...unchecked, ...checked];

  const itemsHtml = sorted.map(item => {
    const p = getProduct(item.productId);
    const [cheapestId] = getCheapestStore(p);
    const [duurId] = getMostExpensiveStore(p);
    const badges = Object.entries(p.prices)
      .sort((a, b) => a[1] - b[1])
      .slice(0, 4) // show top 4 stores
      .map(([sid, price]) => renderStoreBadge(sid, price, sid === cheapestId, sid === duurId))
      .join('');
    return `
      <div class="list-item ${item.checked ? 'checked' : ''} animate-in">
        <input type="checkbox" ${item.checked ? 'checked' : ''} onchange="toggleItem(${p.id})">
        <span class="list-item__emoji">${p.img}</span>
        <div class="list-item__info">
          <div class="list-item__name">${p.name}</div>
          <div class="list-item__meta">${p.size}</div>
          <div class="list-item__badges">${badges}</div>
        </div>
        <button class="list-item__remove" onclick="removeFromList(${p.id})">✕</button>
      </div>`;
  }).join('');

  const split = calculateSplitSavings();
  const bestStore = getStore(split.singleStore);
  const adviesText = optimizeMode === 'single'
    ? `Alles bij ${bestStore.name}: ${formatPrice(split.singleTotal)}`
    : `${split.storesUsed.map(s => getStore(s).short).join(' + ')} = ${formatPrice(split.splitTotal)} — besparing ${formatPrice(split.savings)}!`;

  document.getElementById('screen-lijst').innerHTML = `
    <div class="top-bar">🛒 <span class="screen-title">Mijn Boodschappenlijst</span> <span class="item-count">${unchecked.length} items</span></div>
    <div class="add-item-bar">
      <input type="text" id="add-input" placeholder="Voeg product toe..." oninput="onSearchList(this.value)" autocomplete="off">
      <div id="add-dropdown" class="add-dropdown"></div>
    </div>
    <div class="list-items">${itemsHtml}</div>
    ${unchecked.length > 0 ? `
    <div class="lijst-footer">
      <div class="optimize-toggle">
        <button class="${optimizeMode === 'single' ? 'active' : ''}" onclick="setOptimize('single')">1 Winkel</button>
        <button class="${optimizeMode === 'split' ? 'active' : ''}" onclick="setOptimize('split')">Slim splitsen</button>
      </div>
      <div class="advies">
        <span class="oma-avatar-small">👵</span>
        <div class="advies-text">
          <strong>Oma's Advies</strong><br>
          ${adviesText}
        </div>
      </div>
    </div>` : renderOmaBubble('Je lijst is leeg! Voeg iets toe, lieverd.')}
  `;
}

function onSearchList(query) {
  const dropdown = document.getElementById('add-dropdown');
  if (!query || query.length < 1) { dropdown.innerHTML = ''; return; }
  const matches = PRODUCTS
    .filter(p => p.name.toLowerCase().includes(query.toLowerCase()))
    .filter(p => !shoppingList.find(i => i.productId === p.id))
    .slice(0, 5);
  dropdown.innerHTML = matches.map(p =>
    `<div class="dropdown-item" onclick="addToList(${p.id}); document.getElementById('add-input').value = '';">
      ${p.img} ${p.name} <span class="dropdown-price">${formatPrice(getCheapestStore(p)[1])}</span>
    </div>`
  ).join('');
}

function setOptimize(mode) { optimizeMode = mode; renderLijst(); }
```

**Step 3: Verify**

Open browser. Navigate to Lijst. Should see pre-populated list with 5 items, store price badges, checkbox toggling, autocomplete search, and Oma's Advies footer that updates when toggling optimization mode.

**Step 4: Commit**

```bash
git add prototype/index.html && git commit -m "feat: shopping list screen with price comparison, optimization, and Oma's advies"
```

---

### Task 5: Vergelijk Screen

**Files:**
- Modify: `prototype/index.html` (fill `#screen-vergelijk` + render function)

**Step 1: Build the Vergelijk screen**

Inside `#screen-vergelijk`:
- Top bar: "Vergelijk"
- Large search input: "Zoek een product..."
- Category filter pills: horizontal scroll row (Alles, Zuivel, Brood, Vlees, Groente, Dranken). Click to filter.
- Results area: initially shows all products as `renderProductCard()` cards
- Searching filters products by name match
- Each card has "Oma's Beste Keuze" green badge on the cheapest store
- Each card has "+ Lijst" button that calls `addToList()`
- While "searching" (any keyup), show a brief 300ms "Oma kijkt even rond..." loading message

**Step 2: Add JS**

```js
let activeCategory = 'alles';

function renderVergelijk(query = '') {
  let filtered = PRODUCTS;
  if (activeCategory !== 'alles') {
    filtered = filtered.filter(p => p.category === activeCategory);
  }
  if (query) {
    filtered = filtered.filter(p => p.name.toLowerCase().includes(query.toLowerCase()));
  }

  const categories = ['alles', 'zuivel', 'brood', 'groente', 'dranken'];
  const pillsHtml = categories.map(c =>
    `<button class="category-pill ${c === activeCategory ? 'active' : ''}" onclick="setCategory('${c}')">${c.charAt(0).toUpperCase() + c.slice(1)}</button>`
  ).join('');

  const resultsHtml = filtered.length > 0
    ? filtered.map(p => renderProductCard(p)).join('')
    : renderOmaBubble('Tja, niks gevonden. Probeer iets anders!');

  document.getElementById('screen-vergelijk').innerHTML = `
    <div class="top-bar">🔍 <span class="screen-title">Vergelijk</span></div>
    <div class="search-bar">
      <input type="text" id="search-input" placeholder="Zoek een product..." oninput="onSearchVergelijk(this.value)" value="${query}" autocomplete="off">
    </div>
    <div class="category-pills">${pillsHtml}</div>
    <div class="results">${resultsHtml}</div>
  `;
}

function onSearchVergelijk(query) {
  renderVergelijk(query);
}

function setCategory(cat) {
  activeCategory = cat;
  const input = document.getElementById('search-input');
  renderVergelijk(input ? input.value : '');
}
```

**Step 3: Verify**

Navigate to Vergelijk. Should see all products with store price badges, category pills that filter, search that narrows results, and "+ Lijst" buttons.

**Step 4: Commit**

```bash
git add prototype/index.html && git commit -m "feat: vergelijk screen with search, category filters, and product cards"
```

---

### Task 6: Aanbiedingen Screen

**Files:**
- Modify: `prototype/index.html` (fill `#screen-deals` + render function)

**Step 1: Build the Deals screen**

Inside `#screen-deals`:
- Top bar: "Aanbiedingen"
- Store filter tabs: horizontal scroll (Alles, AH, Jumbo, Lidl, Aldi, Plus, Dirk). Styled as pills with store colors when active.
- "Oma's Toppers" section: top 3 deals (highest discount) with Oma speech bubble: "Dit zijn Oma's toppers deze week!"
- Deals grid: 2-column CSS grid of deal cards using `renderDealCard()`
- Deals with discount >= 40% get the "Hamsteralert!" badge
- Clicking a store tab filters deals to that store

**Step 2: Add JS**

```js
let activeStoreFilter = 'alles';

function renderDeals() {
  let filtered = DEALS;
  if (activeStoreFilter !== 'alles') {
    filtered = filtered.filter(d => d.store === activeStoreFilter);
  }

  const storeTabsHtml = [{ id: 'alles', short: 'Alles', color: 'var(--orange)' }, ...STORES]
    .map(s => `<button class="store-tab ${s.id === activeStoreFilter ? 'active' : ''}" style="${s.id === activeStoreFilter ? 'background:' + s.color + ';color:white' : ''}" onclick="filterDeals('${s.id}')">${s.short}</button>`)
    .join('');

  const toppers = [...DEALS].sort((a, b) => b.discount - a.discount).slice(0, 3);
  const toppersHtml = toppers.map(d => renderDealCard(d)).join('');

  const gridHtml = filtered.map(d => renderDealCard(d)).join('');

  document.getElementById('screen-deals').innerHTML = `
    <div class="top-bar">🏷️ <span class="screen-title">Aanbiedingen</span></div>
    <div class="store-tabs">${storeTabsHtml}</div>
    <div class="toppers-section">
      <h3>Oma's Toppers</h3>
      ${renderOmaBubble('Dit zijn Oma\'s toppers deze week!')}
      <div class="toppers-row">${toppersHtml}</div>
    </div>
    <h3>Alle deals</h3>
    <div class="deals-grid">${gridHtml}</div>
  `;
}

function filterDeals(storeId) {
  activeStoreFilter = storeId;
  renderDeals();
}
```

**Step 3: Verify**

Navigate to Deals. Should see store filter tabs, Oma's Toppers section with top 3 deals, deals grid, Hamsteralert badges on >40% deals.

**Step 4: Commit**

```bash
git add prototype/index.html && git commit -m "feat: aanbiedingen screen with store filters, toppers, and deal grid"
```

---

### Task 7: Mijn Oma Screen

**Files:**
- Modify: `prototype/index.html` (fill `#screen-oma` + render function)

**Step 1: Build the Profile/Savings screen**

Inside `#screen-oma`:
- Large Oma section: centered 👵 emoji (64px) with speech bubble: "Goed bezig, lieverd!" (using Caveat font)
- Lifetime savings: big green number "€847,30 bespaard" (mock data)
- Stats row: 3 mini-cards in grid: "Deze week: €14,20", "Deze maand: €63,40", "Gemiddeld/week: €11,20"
- Bar graph: simple CSS bars showing weekly savings for last 6 weeks (mock data). Bars are green, labeled with week numbers and amounts.
- Thrift level: progress bar (0-100%), current level "Koopjeskoning" (3rd of 4), next level "Gouden Oma". Orange progress bar with level markers.
- Levels: Beginner (0-25%), Slimme Shopper (25-50%), Koopjeskoning (50-75%), Gouden Oma (75-100%)
- Settings section (visual only, non-functional): "Favoriete winkels", "Meldingen"

**Step 2: Add JS**

```js
function renderOmaProfile() {
  const weeklyData = [
    { week: 'W9', amount: 8.40 },
    { week: 'W10', amount: 12.80 },
    { week: 'W11', amount: 9.60 },
    { week: 'W12', amount: 15.30 },
    { week: 'W13', amount: 11.20 },
    { week: 'W14', amount: 14.20 }
  ];
  const maxAmount = Math.max(...weeklyData.map(w => w.amount));
  const barsHtml = weeklyData.map(w =>
    `<div class="bar-col">
      <div class="bar" style="height:${(w.amount / maxAmount) * 120}px"></div>
      <div class="bar-label">${formatPrice(w.amount)}</div>
      <div class="bar-week">${w.week}</div>
    </div>`
  ).join('');

  const level = 62; // percentage
  const levelName = 'Koopjeskoning';
  const nextLevel = 'Gouden Oma';
  const levels = ['Beginner', 'Slimme Shopper', 'Koopjeskoning', 'Gouden Oma'];

  document.getElementById('screen-oma').innerHTML = `
    <div class="top-bar">👵 <span class="screen-title">Mijn Oma</span></div>
    <div class="oma-hero">
      <div class="oma-big">👵</div>
      ${renderOmaBubble('Goed bezig, lieverd! Je bespaart als een echte Oma!')}
    </div>
    <div class="savings-big">
      <span class="savings-amount">€847,30</span>
      <span class="savings-label">totaal bespaard</span>
    </div>
    <div class="stats-row">
      <div class="stat-card"><strong>€14,20</strong><br>Deze week</div>
      <div class="stat-card"><strong>€63,40</strong><br>Deze maand</div>
      <div class="stat-card"><strong>€11,20</strong><br>Gem./week</div>
    </div>
    <h3>Besparingen per week</h3>
    <div class="bar-chart">${barsHtml}</div>
    <h3>Zuinigheidsniveau</h3>
    <div class="level-section">
      <div class="level-bar">
        <div class="level-fill" style="width:${level}%"></div>
      </div>
      <div class="level-labels">
        ${levels.map((l, i) => `<span class="${l === levelName ? 'current-level' : ''}">${l}</span>`).join('')}
      </div>
      <p class="level-text">Nog ${100 - level}% tot <strong>${nextLevel}</strong>!</p>
    </div>
    <h3>Instellingen</h3>
    <div class="settings-section">
      <div class="setting-row">
        <span>Favoriete winkels</span>
        <span class="setting-value">AH, Lidl, Jumbo ›</span>
      </div>
      <div class="setting-row">
        <span>Meldingen</span>
        <span class="setting-value">Wekelijks ›</span>
      </div>
    </div>
  `;
}
```

**Step 3: Verify**

Navigate to Mijn Oma. Should see: Oma greeting, lifetime savings number, stats cards, bar chart, level progress bar, settings rows.

**Step 4: Commit**

```bash
git add prototype/index.html && git commit -m "feat: mijn oma profile screen with savings stats, chart, and thrift levels"
```

---

### Task 8: Toast Notifications & Oma Bubble Overlay

**Files:**
- Modify: `prototype/index.html` (add toast system + floating Oma bubble)

**Step 1: Add toast/bubble overlay system**

- Fixed-position toast container at top center for brief messages ("Toegevoegd aan lijst!", "Binnenkort beschikbaar!")
- Toast auto-dismisses after 2 seconds, slides down from top
- Floating Oma bubble: appears bottom-right (above nav) when triggered, auto-dismisses after 3 seconds
- CSS: `.toast` — white bg, shadow, border-left 4px green, slide-down animation. `.oma-float` — positioned bottom-right, Oma bubble style, fadeIn + slideUp animation.

**Step 2: Add JS**

```js
function showToast(msg) {
  const toast = document.createElement('div');
  toast.className = 'toast animate-in';
  toast.textContent = msg;
  document.getElementById('app').appendChild(toast);
  setTimeout(() => toast.remove(), 2000);
}

function showOmaBubble(msg) {
  // Remove existing bubble
  document.querySelectorAll('.oma-float').forEach(el => el.remove());
  const bubble = document.createElement('div');
  bubble.className = 'oma-float animate-in';
  bubble.innerHTML = `<span class="oma-avatar">👵</span> <span style="font-family:'Caveat',cursive;font-size:18px">${msg}</span>`;
  document.getElementById('app').appendChild(bubble);
  setTimeout(() => bubble.remove(), 3000);
}
```

**Step 3: Update `addToList` to show both toast and Oma bubble**

When adding an item: `showToast('Toegevoegd aan lijst!')` + `showOmaBubble('Slim bezig, lieverd!')`.

**Step 4: Verify**

Add a product from Vergelijk. Should see green toast at top + Oma bubble bottom-right, both auto-dismiss.

**Step 5: Commit**

```bash
git add prototype/index.html && git commit -m "feat: toast notifications and floating Oma speech bubble overlay"
```

---

### Task 9: Polish, Responsive, & Final Touches

**Files:**
- Modify: `prototype/index.html` (CSS polish + responsive)

**Step 1: Mobile-first responsive polish**

- Base: 375px mobile. Max-width: 480px centered on desktop.
- `#app` — `max-width: 480px; margin: 0 auto; position: relative; min-height: 100vh;`
- Bottom nav: `position: fixed; bottom: 0; width: 100%; max-width: 480px;`
- Ensure all touch targets are 44px minimum
- Add subtle background pattern: faint repeating `🌷` at 3% opacity using CSS pseudo-element or background-image
- Smooth screen transitions: fade in/out (150ms)
- Add `<meta name="theme-color" content="#FF6200">` for browser chrome
- Add `<meta name="apple-mobile-web-app-capable" content="yes">`
- Add `<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>👵</text></svg>">`
- Page title: "Oma Zuinig — Kijken? Oma koopt slimmer!"

**Step 2: Visual polish**

- Ensure consistent spacing (8px grid system: 8, 16, 24, 32)
- Card hover states on desktop (subtle shadow lift)
- Active tab in bottom nav: orange text + dot indicator
- Smooth scrolling for deal carousels
- Price colors: green for cheap, red+strikethrough for expensive
- Hero banner: subtle gradient animation (shimmer effect, very subtle)

**Step 3: Call all render functions on page load**

```js
document.addEventListener('DOMContentLoaded', () => {
  renderHome();
  renderLijst();
  renderVergelijk();
  renderDeals();
  renderOmaProfile();
  navigate('home'); // show home first
});
```

**Step 4: Full browser test**

Open prototype/index.html. Test all 5 screens, navigation, adding items, searching, filtering, toggling optimization. Everything should feel smooth, warm, and distinctly Dutch.

**Step 5: Commit**

```bash
git add prototype/index.html && git commit -m "feat: responsive polish, background patterns, meta tags, final touches"
```

---

## Task Dependency Summary

```
Task 0 (Shell) → Task 1 (Data) → Task 2 (Components) → Task 3-7 (Screens, parallel) → Task 8 (Toast/Bubble) → Task 9 (Polish)
```

Tasks 3-7 can technically be built in parallel since they're independent screens, but they share components from Task 2.
