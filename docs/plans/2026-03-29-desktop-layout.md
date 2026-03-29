# Desktop Responsive Layout — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:executing-plans to implement this plan task-by-task.

**Goal:** Make the Oma Zuinig app fully responsive — proper desktop layout with top nav, dashboard home, and adaptive page layouts, while keeping the mobile experience untouched.

**Architecture:** Single breakpoint at 768px. Below = current mobile (480px shell + bottom nav). Above = wide shell (1200px max) + DesktopNav top bar. Each page gets desktop-specific CSS grid layouts via media queries in its own `<style>` block.

**Tech Stack:** SvelteKit (Svelte 5), plain CSS with existing custom properties, no new dependencies.

---

### Task 1: Add desktop breakpoint variable and widen the app shell

**Files:**
- Modify: `app/src/app.css` (add breakpoint variable)
- Modify: `app/src/routes/+layout.svelte` (responsive shell)

**Step 1: Add breakpoint custom property to app.css**

In `app/src/app.css`, add to the `:root` block:

```css
--bp-desktop: 768px;
--content-max: 1200px;
```

**Step 2: Make app-shell responsive in +layout.svelte**

Replace the `.app-shell` style:

```css
.app-shell {
  max-width: 480px;
  margin: 0 auto;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  background: linear-gradient(180deg, white 0%, #FFF9F5 40%, #FFFAF7 100%);
}

@media (min-width: 768px) {
  .app-shell {
    max-width: 1200px;
    padding: 0 var(--space-8);
  }
}
```

**Step 3: Hide mobile header on desktop**

Add media query to hide `.app-header` on desktop (DesktopNav will replace it):

```css
@media (min-width: 768px) {
  .app-header {
    display: none;
  }
}
```

**Step 4: Verify mobile is unchanged**

Run: `cd /c/omazuinig/app && npm run dev`
Check at narrow viewport — should look identical.

**Step 5: Commit**

```bash
git add app/src/app.css app/src/routes/+layout.svelte
git commit -m "feat: add desktop breakpoint, widen app shell above 768px"
```

---

### Task 2: Create DesktopNav component

**Files:**
- Create: `app/src/lib/components/DesktopNav.svelte`
- Modify: `app/src/routes/+layout.svelte` (import and add DesktopNav)

**Step 1: Create DesktopNav.svelte**

```svelte
<script lang="ts">
  import { page } from '$app/stores';

  const links = [
    { href: '/', label: 'Home', icon: 'home' },
    { href: '/lijst', label: 'Lijst', icon: 'lijst' },
    { href: '/vergelijk', label: 'Vergelijk', icon: 'vergelijk' },
    { href: '/deals', label: 'Deals', icon: 'deals' },
    { href: '/mijn-oma', label: 'Mijn Oma', icon: 'mijnoma' }
  ];
</script>

<nav class="desktop-nav" aria-label="Hoofdnavigatie">
  <div class="nav-inner">
    <a href="/" class="nav-brand">
      <img src="/oma-avatar.png" alt="" class="nav-oma" />
      <span class="nav-title">Oma Zuinig</span>
    </a>
    <div class="nav-links">
      {#each links as link}
        <a
          href={link.href}
          class="nav-item"
          class:active={$page.url.pathname === link.href}
          aria-current={$page.url.pathname === link.href ? 'page' : undefined}
        >
          {link.label}
        </a>
      {/each}
    </div>
    <div class="nav-right"></div>
  </div>
</nav>

<style>
  .desktop-nav {
    display: none;
    position: sticky;
    top: 0;
    z-index: 100;
    background: white;
    border-bottom: 1px solid var(--gray-200);
  }

  @media (min-width: 768px) {
    .desktop-nav {
      display: block;
    }
  }

  .nav-inner {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    height: 64px;
    padding: 0 var(--space-8);
    gap: var(--space-8);
  }

  .nav-brand {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    text-decoration: none;
    flex-shrink: 0;
  }

  .nav-oma {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    object-fit: cover;
  }

  .nav-title {
    font-size: 22px;
    font-weight: 700;
    color: var(--orange);
    letter-spacing: -0.02em;
  }

  .nav-links {
    display: flex;
    align-items: center;
    gap: var(--space-1);
  }

  .nav-item {
    padding: var(--space-2) var(--space-4);
    text-decoration: none;
    font-size: 15px;
    font-weight: 600;
    color: var(--gray-600);
    border-radius: var(--radius-lg);
    transition: all var(--transition-fast);
  }

  .nav-item:hover {
    color: var(--dark);
    background: var(--gray-50);
  }

  .nav-item.active {
    color: var(--orange);
    background: var(--orange-light);
  }

  .nav-right {
    margin-left: auto;
  }
</style>
```

**Step 2: Add DesktopNav to +layout.svelte**

Import DesktopNav and add it before the app-shell content. Also hide BottomNav on desktop:

```svelte
<script lang="ts">
  import '../app.css';
  import { page } from '$app/stores';
  import BottomNav from '$lib/components/BottomNav.svelte';
  import DesktopNav from '$lib/components/DesktopNav.svelte';
  import Toast from '$lib/components/Toast.svelte';
  import Celebration from '$lib/components/Celebration.svelte';

  let { children } = $props();

  const titles: Record<string, string> = {
    '/': 'Oma Zuinig',
    '/lijst': 'Boodschappenlijst',
    '/vergelijk': 'Vergelijk',
    '/deals': 'Aanbiedingen',
    '/mijn-oma': 'Mijn Oma'
  };

  let title = $derived(titles[$page.url.pathname] ?? 'Oma Zuinig');
</script>

<DesktopNav />
<div class="app-shell">
  <header class="app-header">
    <img src="/oma-avatar.png" alt="" class="header-oma" />
    <span class="header-title">{title}</span>
  </header>
  {@render children()}
  <BottomNav />
  <Toast />
  <Celebration />
</div>
```

**Step 3: Hide BottomNav on desktop**

Add to `BottomNav.svelte` styles:

```css
@media (min-width: 768px) {
  .bottom-nav {
    display: none;
  }
}
```

**Step 4: Verify both layouts**

- Narrow viewport: mobile header + bottom nav visible, desktop nav hidden
- Wide viewport: desktop nav visible, mobile header + bottom nav hidden

**Step 5: Commit**

```bash
git add app/src/lib/components/DesktopNav.svelte app/src/routes/+layout.svelte app/src/lib/components/BottomNav.svelte
git commit -m "feat: add DesktopNav, hide bottom nav on desktop"
```

---

### Task 3: Desktop layout for Home page (dashboard grid)

**Files:**
- Modify: `app/src/routes/+page.svelte`

**Step 1: Add desktop media queries to Home page**

Add these media queries to the existing `<style>` block:

```css
@media (min-width: 768px) {
  .page {
    padding-bottom: var(--space-8);
  }

  .hero {
    min-height: 200px;
    padding: var(--space-8);
  }

  .hero-amount {
    font-size: 64px;
  }

  .hero-oma {
    width: 110px;
    height: 110px;
  }

  .deals-carousel {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    overflow-x: visible;
    margin: 0;
    padding-left: 0;
    padding-right: 0;
  }

  .deals-carousel::after {
    display: none;
  }

  .deal-slide {
    width: auto;
  }

  .products-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-4);
  }
}
```

**Step 2: Verify dashboard layout**

Wide viewport: deals in 4-col grid, products in 2-col grid, hero wider.
Narrow viewport: unchanged carousel + stacked list.

**Step 3: Commit**

```bash
git add app/src/routes/+page.svelte
git commit -m "feat: desktop dashboard layout for Home — grid deals, 2-col products"
```

---

### Task 4: Desktop layout for Vergelijk page

**Files:**
- Modify: `app/src/routes/vergelijk/+page.svelte`

**Step 1: Add desktop media queries**

```css
@media (min-width: 768px) {
  .page {
    padding-bottom: var(--space-8);
  }

  .search-input {
    max-width: 500px;
  }

  .product-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-4);
  }
}
```

**Step 2: Verify and commit**

```bash
git add app/src/routes/vergelijk/+page.svelte
git commit -m "feat: desktop layout for Vergelijk — 2-col product grid"
```

---

### Task 5: Desktop layout for Deals page

**Files:**
- Modify: `app/src/routes/deals/+page.svelte`

**Step 1: Add desktop media queries**

```css
@media (min-width: 768px) {
  .page {
    padding-bottom: var(--space-8);
  }

  .toppers-list {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-4);
  }

  .deals-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-4);
  }
}
```

**Step 2: Verify and commit**

```bash
git add app/src/routes/deals/+page.svelte
git commit -m "feat: desktop layout for Deals — 3-col toppers, 4-col grid"
```

---

### Task 6: Desktop layout for Lijst page

**Files:**
- Modify: `app/src/routes/lijst/+page.svelte`

**Step 1: Add desktop media queries**

On desktop, the advice panel should sit as a sidebar instead of sticky bottom:

```css
@media (min-width: 768px) {
  .page {
    padding-bottom: var(--space-8);
    display: grid;
    grid-template-columns: 1fr 340px;
    grid-template-rows: auto 1fr;
    gap: var(--space-6);
  }

  .search-wrapper {
    grid-column: 1 / -1;
  }

  .list {
    grid-column: 1;
  }

  .advice-panel {
    grid-column: 2;
    grid-row: 2;
    position: sticky;
    top: 88px;
    bottom: auto;
    border-top: none;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-lg);
    align-self: start;
  }
}
```

**Step 2: Verify and commit**

```bash
git add app/src/routes/lijst/+page.svelte
git commit -m "feat: desktop layout for Lijst — sidebar advice panel"
```

---

### Task 7: Desktop layout for Mijn Oma page

**Files:**
- Modify: `app/src/routes/mijn-oma/+page.svelte`

**Step 1: Add desktop media queries**

Center the content with a max-width, put stats and chart side by side:

```css
@media (min-width: 768px) {
  .page {
    max-width: 800px;
    margin: 0 auto;
    padding-bottom: var(--space-8);
  }

  .stats-row {
    gap: var(--space-8);
  }

  .chart-section {
    padding: var(--space-8);
  }

  .chart {
    height: 180px;
  }

  .bar {
    width: 24px;
  }
}
```

**Step 2: Verify and commit**

```bash
git add app/src/routes/mijn-oma/+page.svelte
git commit -m "feat: desktop layout for Mijn Oma — wider chart, centered content"
```

---

### Task 8: Final polish and push

**Step 1: Test all pages at both breakpoints**

Run dev server, check:
- Each page at 375px (mobile)
- Each page at 1280px (desktop)
- Resize smoothly across breakpoint

**Step 2: Fix any visual issues found**

**Step 3: Commit any polish fixes and push**

```bash
git push origin master
```

Vercel auto-deploys from master — changes go live at omazuinig.vercel.app.
