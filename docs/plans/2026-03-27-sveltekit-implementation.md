# Oma Zuinig SvelteKit App — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:executing-plans to implement this plan task-by-task.

**Goal:** Build the production Oma Zuinig SvelteKit app with 5 pages, component library, mock data layer, PWA support, and the full design system.

**Architecture:** SvelteKit app with TypeScript. Mock data behind interfaces that match future Supabase schema. Svelte stores for reactive state (shopping list, toasts). File-based routing. PWA manifest + service worker for installability and offline lists. Deployed to Vercel.

**Tech Stack:** SvelteKit, TypeScript, Vite, Google Fonts (Inter + Caveat), Vercel adapter

---

### Task 0: Scaffold SvelteKit Project

**Files:**
- Create: `package.json`, `svelte.config.js`, `vite.config.js`, `tsconfig.json`, `src/app.html`, `src/app.css`

**Step 1: Initialize SvelteKit project**

```bash
cd /c/omazuinig
npm create svelte@latest app -- --template skeleton --types typescript --no-add-ons
```

This creates the `app/` directory. We build inside `app/` to keep docs/plans/prototype separate.

**Step 2: Install dependencies**

```bash
cd /c/omazuinig/app
npm install
npm install -D @sveltejs/adapter-vercel
```

**Step 3: Configure Vercel adapter**

Update `svelte.config.js`:
```js
import adapter from '@sveltejs/adapter-vercel';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
  preprocess: vitePreprocess(),
  kit: { adapter: adapter() }
};
```

**Step 4: Verify it runs**

```bash
cd /c/omazuinig/app && npm run dev
```
Expected: Dev server starts on localhost:5173, shows SvelteKit welcome page.

**Step 5: Commit**

```bash
cd /c/omazuinig && git add app/ && git commit -m "feat: scaffold SvelteKit project with Vercel adapter"
```

---

### Task 1: Design System (app.css + app.html)

**Files:**
- Modify: `app/src/app.html`
- Modify: `app/src/app.css`

**Step 1: Update app.html**

Set up the HTML shell with Google Fonts, meta tags, and favicon:

```html
<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#FF6200" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="description" content="Vergelijk boodschappenprijzen bij alle Nederlandse supermarkten. Oma Zuinig vindt de goedkoopste winkel voor jouw boodschappenlijst." />
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>👵</text></svg>" />
    <link rel="manifest" href="%sveltekit.assets%/manifest.json" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Caveat&display=swap" rel="stylesheet" />
    %sveltekit.head%
  </head>
  <body data-sveltekit-preload-data="hover">
    <div style="display: contents">%sveltekit.body%</div>
  </body>
</html>
```

**Step 2: Write app.css with full design system**

```css
:root {
  --orange: #FF6200;
  --green: #00C853;
  --blue: #0052CC;
  --cream: #FFF9F0;
  --red: #E6392E;
  --dark: #1C1C1C;
  --shadow-sm: 0 1px 4px rgba(0,0,0,0.06);
  --shadow-md: 0 2px 8px rgba(0,0,0,0.08);
  --shadow-lg: 0 4px 16px rgba(0,0,0,0.12);
  --radius-sm: 12px;
  --radius-md: 16px;
  --radius-lg: 20px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', sans-serif;
  background: var(--cream);
  color: var(--dark);
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3 { font-weight: 700; }
h1 { font-size: 24px; }
h2 { font-size: 20px; }
h3 { font-size: 18px; }

.oma-text { font-family: 'Caveat', cursive; }

@keyframes slideUp {
  from { transform: translateY(16px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
@keyframes slideDown {
  from { transform: translateX(-50%) translateY(-20px); opacity: 0; }
  to { transform: translateX(-50%) translateY(0); opacity: 1; }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

**Step 3: Verify**

```bash
cd /c/omazuinig/app && npm run dev
```
Page should show with cream background and Inter font.

**Step 4: Commit**

```bash
git add app/src/app.html app/src/app.css && git commit -m "feat: design system — colors, typography, animations, meta tags"
```

---

### Task 2: Data Layer (types, mock data, utils)

**Files:**
- Create: `app/src/lib/data/types.ts`
- Create: `app/src/lib/data/stores.ts`
- Create: `app/src/lib/data/products.ts`
- Create: `app/src/lib/data/deals.ts`
- Create: `app/src/lib/utils/price.ts`

**Step 1: Create types.ts**

```typescript
export interface Store {
  id: string;
  name: string;
  short: string;
  color: string;
}

export interface Product {
  id: number;
  name: string;
  brand: string;
  size: string;
  category: string;
  image: string;
  prices: Record<string, number>;
}

export interface Deal {
  productId: number;
  store: string;
  oldPrice: number;
  newPrice: number;
  discount: number;
}

export interface ShoppingListItem {
  productId: number;
  checked: boolean;
}
```

**Step 2: Create stores.ts (supermarket data)**

```typescript
import type { Store } from './types';

export const STORES: Store[] = [
  { id: 'ah', name: 'Albert Heijn', short: 'AH', color: '#00A0E2' },
  { id: 'jumbo', name: 'Jumbo', short: 'Jumbo', color: '#FFD700' },
  { id: 'lidl', name: 'Lidl', short: 'Lidl', color: '#0050AA' },
  { id: 'aldi', name: 'Aldi', short: 'Aldi', color: '#00599C' },
  { id: 'plus', name: 'Plus', short: 'Plus', color: '#E3000B' },
  { id: 'dirk', name: 'Dirk', short: 'Dirk', color: '#E31937' }
];

export function getStore(id: string): Store | undefined {
  return STORES.find(s => s.id === id);
}
```

**Step 3: Create products.ts**

```typescript
import type { Product } from './types';

export const PRODUCTS: Product[] = [
  { id: 1, name: 'Halfvolle melk', brand: 'Huismerk', size: '1L', category: 'zuivel', image: '🥛', prices: { ah: 1.29, jumbo: 1.25, lidl: 0.99, aldi: 0.95, plus: 1.19, dirk: 1.09 } },
  { id: 2, name: 'Gouda kaas jong belegen', brand: 'Huismerk', size: '500g', category: 'zuivel', image: '🧀', prices: { ah: 4.99, jumbo: 4.79, lidl: 3.99, aldi: 3.89, plus: 4.49, dirk: 4.29 } },
  { id: 3, name: 'Volkoren brood', brand: 'Huismerk', size: '800g', category: 'brood', image: '🍞', prices: { ah: 1.89, jumbo: 1.79, lidl: 1.49, aldi: 1.39, plus: 1.69, dirk: 1.59 } },
  { id: 4, name: 'Scharreleieren', brand: 'Huismerk', size: '10 stuks', category: 'zuivel', image: '🥚', prices: { ah: 3.29, jumbo: 2.99, lidl: 2.69, aldi: 2.59, plus: 2.89, dirk: 2.79 } },
  { id: 5, name: 'Heineken Pilsener', brand: 'Heineken', size: '6-pack', category: 'dranken', image: '🍺', prices: { ah: 5.99, jumbo: 5.49, lidl: 5.29, aldi: 5.19, plus: 5.69, dirk: 5.39 } },
  { id: 6, name: 'Aroma Rood koffie', brand: 'Douwe Egberts', size: '500g', category: 'dranken', image: '☕', prices: { ah: 6.99, jumbo: 6.49, lidl: 5.99, aldi: 5.79, plus: 6.29, dirk: 6.19 } },
  { id: 7, name: 'Pindakaas', brand: 'Calvé', size: '650g', category: 'brood', image: '🥜', prices: { ah: 4.49, jumbo: 3.99, lidl: 3.79, aldi: 3.69, plus: 4.19, dirk: 3.89 } },
  { id: 8, name: 'Paprika rood', brand: '', size: 'per stuk', category: 'groente', image: '🫑', prices: { ah: 1.19, jumbo: 0.99, lidl: 0.89, aldi: 0.85, plus: 0.99, dirk: 0.95 } },
  { id: 9, name: 'Melkchocolade hagelslag', brand: 'De Ruijter', size: '400g', category: 'brood', image: '🍫', prices: { ah: 2.99, jumbo: 2.79, lidl: 2.49, aldi: 2.39, plus: 2.69, dirk: 2.59 } },
  { id: 10, name: 'Karnemelk', brand: 'Huismerk', size: '1L', category: 'zuivel', image: '🥛', prices: { ah: 1.09, jumbo: 0.99, lidl: 0.89, aldi: 0.85, plus: 0.99, dirk: 0.95 } }
];

export function getProduct(id: number): Product | undefined {
  return PRODUCTS.find(p => p.id === id);
}
```

**Step 4: Create deals.ts**

```typescript
import type { Deal } from './types';

export const DEALS: Deal[] = [
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

**Step 5: Create price.ts utilities**

```typescript
import type { Product } from '$lib/data/types';
import { STORES } from '$lib/data/stores';

export function formatPrice(n: number): string {
  return '€' + n.toFixed(2).replace('.', ',');
}

export function getCheapestStore(product: Product): [string, number] {
  return Object.entries(product.prices).sort((a, b) => a[1] - b[1])[0];
}

export function getMostExpensiveStore(product: Product): [string, number] {
  return Object.entries(product.prices).sort((a, b) => b[1] - a[1])[0];
}

export function calculateBestSingleStore(items: { productId: number; checked: boolean }[], getProduct: (id: number) => Product | undefined): [string, number][] {
  const unchecked = items.filter(i => !i.checked);
  const storeTotals: Record<string, number> = {};
  STORES.forEach(s => { storeTotals[s.id] = 0; });
  unchecked.forEach(item => {
    const product = getProduct(item.productId);
    if (!product) return;
    STORES.forEach(s => { storeTotals[s.id] += product.prices[s.id] ?? 0; });
  });
  return Object.entries(storeTotals).sort((a, b) => a[1] - b[1]);
}

export function calculateSplitSavings(items: { productId: number; checked: boolean }[], getProduct: (id: number) => Product | undefined) {
  const unchecked = items.filter(i => !i.checked);
  let splitTotal = 0;
  const storesUsed = new Set<string>();
  unchecked.forEach(item => {
    const product = getProduct(item.productId);
    if (!product) return;
    const [cheapestId, cheapestPrice] = getCheapestStore(product);
    splitTotal += cheapestPrice;
    storesUsed.add(cheapestId);
  });
  const bestStoreResult = calculateBestSingleStore(items, getProduct);
  const [singleStore, singleTotal] = bestStoreResult[0] ?? ['', 0];
  return {
    splitTotal,
    storesUsed: [...storesUsed],
    singleStore,
    singleTotal,
    savings: singleTotal - splitTotal
  };
}
```

**Step 6: Verify TypeScript compiles**

```bash
cd /c/omazuinig/app && npx svelte-check
```

**Step 7: Commit**

```bash
git add app/src/lib/ && git commit -m "feat: data layer — types, mock data, price utilities"
```

---

### Task 3: Svelte Stores (shopping list, toast)

**Files:**
- Create: `app/src/lib/stores/shoppingList.ts`
- Create: `app/src/lib/stores/toast.ts`

**Step 1: Create shoppingList.ts**

Writable store with localStorage persistence:

```typescript
import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import type { ShoppingListItem } from '$lib/data/types';

const defaultItems: ShoppingListItem[] = [
  { productId: 1, checked: false },
  { productId: 2, checked: false },
  { productId: 4, checked: false },
  { productId: 7, checked: false },
  { productId: 6, checked: true }
];

function createShoppingList() {
  const stored = browser ? localStorage.getItem('oma-shopping-list') : null;
  const initial: ShoppingListItem[] = stored ? JSON.parse(stored) : defaultItems;

  const { subscribe, set, update } = writable<ShoppingListItem[]>(initial);

  if (browser) {
    subscribe(value => {
      localStorage.setItem('oma-shopping-list', JSON.stringify(value));
    });
  }

  return {
    subscribe,
    add: (productId: number) => update(items => {
      if (items.find(i => i.productId === productId)) return items;
      return [...items, { productId, checked: false }];
    }),
    toggle: (productId: number) => update(items =>
      items.map(i => i.productId === productId ? { ...i, checked: !i.checked } : i)
    ),
    remove: (productId: number) => update(items =>
      items.filter(i => i.productId !== productId)
    ),
    clear: () => set([])
  };
}

export const shoppingList = createShoppingList();
```

**Step 2: Create toast.ts**

```typescript
import { writable } from 'svelte/store';

interface ToastMessage {
  id: number;
  text: string;
  type: 'success' | 'info';
}

function createToastStore() {
  const { subscribe, update } = writable<ToastMessage[]>([]);
  let nextId = 0;

  return {
    subscribe,
    show: (text: string, type: 'success' | 'info' = 'success') => {
      const id = nextId++;
      update(toasts => [...toasts, { id, text, type }]);
      setTimeout(() => {
        update(toasts => toasts.filter(t => t.id !== id));
      }, 2500);
    }
  };
}

export const toasts = createToastStore();
```

**Step 3: Commit**

```bash
git add app/src/lib/stores/ && git commit -m "feat: Svelte stores — shopping list with localStorage, toast notifications"
```

---

### Task 4: Component Library

**Files:**
- Create: `app/src/lib/components/StoreBadge.svelte`
- Create: `app/src/lib/components/ProductCard.svelte`
- Create: `app/src/lib/components/DealCard.svelte`
- Create: `app/src/lib/components/OmaBubble.svelte`
- Create: `app/src/lib/components/CategoryPills.svelte`
- Create: `app/src/lib/components/ListItem.svelte`
- Create: `app/src/lib/components/BottomNav.svelte`
- Create: `app/src/lib/components/Toast.svelte`

Build all 8 components. Each is a single `.svelte` file with TypeScript, scoped CSS, and clear props. Components should use the design system variables from app.css. Full implementation details:

**StoreBadge**: Takes `store: Store`, `price: number`, `cheapest: boolean`, `duur: boolean`. Renders colored pill.

**ProductCard**: Takes `product: Product`. Shows emoji, name, brand/size, all store badges sorted by price, green "Oma's Keuze" on cheapest, "+ Lijst" button that dispatches to shoppingList store + toasts.

**DealCard**: Takes `deal: Deal`. Shows product emoji, store name, old/new price, discount badge, Hamsteralert if >= 40%.

**OmaBubble**: Takes `text: string`. Oma avatar + speech bubble in Caveat font.

**CategoryPills**: Takes `categories: string[]`, `active: string`. Dispatches `select` event. Horizontal scroll row.

**ListItem**: Takes `item: ShoppingListItem`, `product: Product`. Checkbox, emoji, name, top 4 store badges, remove button. Dispatches `toggle` and `remove` events.

**BottomNav**: 5 tabs, uses `$page.url.pathname` to highlight active. Links to /, /lijst, /vergelijk, /deals, /mijn-oma.

**Toast**: Subscribes to toasts store, renders fixed-position notifications that auto-dismiss.

**Step: Verify components compile**

```bash
cd /c/omazuinig/app && npx svelte-check
```

**Commit:**

```bash
git add app/src/lib/components/ && git commit -m "feat: component library — StoreBadge, ProductCard, DealCard, OmaBubble, CategoryPills, ListItem, BottomNav, Toast"
```

---

### Task 5: Layout + Bottom Nav + Toast Layer

**Files:**
- Create: `app/src/routes/+layout.svelte`

**Step 1: Create the layout**

```svelte
<script lang="ts">
  import '../app.css';
  import BottomNav from '$lib/components/BottomNav.svelte';
  import Toast from '$lib/components/Toast.svelte';

  let { children } = $props();
</script>

<div class="app-shell">
  {@render children()}
  <BottomNav />
  <Toast />
</div>

<style>
  .app-shell {
    max-width: 480px;
    margin: 0 auto;
    min-height: 100vh;
    position: relative;
    padding-bottom: 68px;
  }
</style>
```

**Step 2: Verify**

```bash
cd /c/omazuinig/app && npm run dev
```
Should see bottom nav and cream background.

**Step 3: Commit**

```bash
git add app/src/routes/+layout.svelte && git commit -m "feat: app layout with bottom nav and toast layer"
```

---

### Task 6: Home Page

**Files:**
- Modify: `app/src/routes/+page.svelte`

Home page with:
- Top bar: "👵 Oma Zuinig" logo
- Hero banner (orange gradient): greeting + savings amount
- 3 quick-action cards (grid) linking to /lijst, /vergelijk, and scan placeholder
- Section header with OmaBubble
- Horizontal scrolling deals carousel using DealCard components
- All data imported from mock data layer

**Verify:**

```bash
npm run dev
```
Home screen should match the prototype design.

**Commit:**

```bash
git add app/src/routes/+page.svelte && git commit -m "feat: home page — hero banner, quick actions, deals carousel"
```

---

### Task 7: Lijst Page (Shopping List)

**Files:**
- Create: `app/src/routes/lijst/+page.svelte`

The most complex page. Uses the shoppingList Svelte store:
- Add-item search bar with autocomplete dropdown (filter PRODUCTS by name)
- List of ListItem components (unchecked first, then checked)
- Sticky footer with optimize toggle ("Eén winkel" / "Max besparing")
- Oma's Advies showing calculated best store or split optimization
- All reactive — adding/removing/toggling items recalculates instantly

**Verify:**

```bash
npm run dev
```
Navigate to /lijst. Pre-populated list, add items via search, toggle checkboxes, see Oma's Advies update.

**Commit:**

```bash
git add app/src/routes/lijst/ && git commit -m "feat: shopping list page with optimization and Oma's advies"
```

---

### Task 8: Vergelijk Page (Search & Compare)

**Files:**
- Create: `app/src/routes/vergelijk/+page.svelte`

- Search bar with reactive filtering
- CategoryPills component for category filter
- ProductCard components for results
- Empty state with OmaBubble
- Supports `?q=` query param via `$page.url.searchParams`

**Verify:**

Navigate to /vergelijk. Search for "melk", filter by category. Products show with store badges.

**Commit:**

```bash
git add app/src/routes/vergelijk/ && git commit -m "feat: vergelijk page with search and category filters"
```

---

### Task 9: Deals Page

**Files:**
- Create: `app/src/routes/deals/+page.svelte`

- Store filter tabs (Alles + each store)
- Oma's Toppers section (top 3 deals by discount) with OmaBubble
- Deals grid (2 columns) with DealCard components
- Hamsteralert badges on deals >= 40% off

**Commit:**

```bash
git add app/src/routes/deals/ && git commit -m "feat: deals page with store filters and Oma's toppers"
```

---

### Task 10: Mijn Oma Page (Profile)

**Files:**
- Create: `app/src/routes/mijn-oma/+page.svelte`

- Oma hero with speech bubble
- Lifetime savings counter (€847,30 mock)
- Stats cards row (3 cards)
- Weekly savings bar chart (CSS bars, mock data)
- Thrift level progress bar (Koopjeskoning, 62%)
- Settings section (visual only)

**Commit:**

```bash
git add app/src/routes/mijn-oma/ && git commit -m "feat: mijn oma profile with savings stats and thrift levels"
```

---

### Task 11: PWA Manifest + Static Assets

**Files:**
- Create: `app/static/manifest.json`
- Create: `app/static/favicon.svg`

**Step 1: Create manifest.json**

```json
{
  "name": "Oma Zuinig",
  "short_name": "Oma Zuinig",
  "description": "Vergelijk boodschappenprijzen bij alle Nederlandse supermarkten",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#FFF9F0",
  "theme_color": "#FF6200",
  "icons": [
    { "src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml" }
  ]
}
```

**Step 2: Create favicon.svg**

Simple SVG with 👵 emoji as the icon.

**Step 3: Verify**

Open Chrome DevTools → Application → Manifest. Should show app info.

**Commit:**

```bash
git add app/static/ && git commit -m "feat: PWA manifest and favicon"
```

---

### Task 12: Final Integration + Build Verification

**Step 1: Run full build**

```bash
cd /c/omazuinig/app && npm run build
```
Expected: Build succeeds with no errors.

**Step 2: Preview production build**

```bash
npm run preview
```
Test all 5 pages, navigation, adding items, search, filtering.

**Step 3: Run type check**

```bash
npx svelte-check
```
Expected: No errors.

**Step 4: Final commit**

```bash
git add -A && git commit -m "feat: Oma Zuinig SvelteKit app — complete MVP with 5 pages, component library, mock data, PWA"
```

---

## Task Dependency Summary

```
Task 0 (Scaffold) → Task 1 (Design System) → Task 2 (Data Layer) → Task 3 (Stores) → Task 4 (Components) → Task 5 (Layout) → Tasks 6-10 (Pages, sequential) → Task 11 (PWA) → Task 12 (Build Verify)
```
