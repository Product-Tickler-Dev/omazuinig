# Oma Zuinig SvelteKit App — Design Document

**Date**: 2026-03-27
**Type**: Production SvelteKit web application
**Goal**: Build the real Oma Zuinig app with proper architecture, mock data, PWA support, ready for Supabase integration.

---

## Tech Stack

- **SvelteKit** — framework (SSR, routing, server endpoints)
- **TypeScript** — type safety, interfaces for future Supabase swap
- **Vercel** — deployment (later)
- **Supabase** — database/auth (scaffolded, mock data for now)
- **Google Fonts** — Inter + Caveat

## Project Structure

```
omazuinig/
├── src/
│   ├── lib/
│   │   ├── components/      → StoreBadge, ProductCard, DealCard, OmaBubble, etc.
│   │   ├── data/            → Mock data + TypeScript interfaces
│   │   │   ├── types.ts     → Store, Product, Deal interfaces
│   │   │   ├── stores.ts    → STORES array
│   │   │   ├── products.ts  → PRODUCTS array
│   │   │   └── deals.ts     → DEALS array
│   │   ├── stores/          → Svelte stores (shopping list, toast, preferences)
│   │   └── utils/           → formatPrice, getCheapest, calculations
│   ├── routes/
│   │   ├── +layout.svelte   → Bottom nav, global wrapper
│   │   ├── +page.svelte     → Home
│   │   ├── lijst/+page.svelte
│   │   ├── vergelijk/+page.svelte
│   │   ├── deals/+page.svelte
│   │   └── mijn-oma/+page.svelte
│   └── app.css              → Design system
├── static/
│   ├── favicon.svg
│   └── manifest.json
├── svelte.config.js
├── package.json
└── vite.config.js
```

## Data Layer

TypeScript interfaces match future Supabase schema:

```typescript
interface Store { id: string; name: string; short: string; color: string; }
interface Product { id: number; name: string; brand: string; size: string; category: string; image: string; prices: Record<string, number>; }
interface Deal { productId: number; store: string; oldPrice: number; newPrice: number; discount: number; }
```

Mock data in `/data/` files. Shopping list in Svelte writable store with localStorage persistence.

## Components

| Component | Purpose |
|-----------|---------|
| StoreBadge | Colored pill: store name + price |
| ProductCard | Product with all store prices + add-to-list |
| DealCard | Deal with old/new price, discount badge, Hamsteralert |
| OmaBubble | Oma speech bubble (Caveat font) |
| CategoryPills | Horizontal filter pills |
| ListItem | Shopping list row with checkbox + prices |
| BottomNav | 5-tab fixed navigation |
| Toast | Global notification system |

## Pages

1. **/** — Home: hero banner, quick actions, deals carousel
2. **/lijst** — Shopping list with optimization (single store vs split)
3. **/vergelijk** — Search + category filter + product cards
4. **/deals** — Store tabs + Oma's Toppers + deals grid
5. **/mijn-oma** — Savings dashboard, thrift level, settings

## PWA

- manifest.json (name, icons, theme color)
- Service worker for offline shopping list
- Installable from browser

## Design System

Colors: --orange #FF6200, --green #00C853, --blue #0052CC, --cream #FFF9F0, --red #E6392E, --dark #1C1C1C
Typography: Inter (400, 700), Caveat (Oma speech)
Spacing: 8px grid
Border radius: 16px cards, 12px badges, 20px pills
