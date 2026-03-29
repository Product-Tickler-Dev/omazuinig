<script lang="ts">
  import { PRODUCTS } from '$lib/data/products';
  import { DEALS } from '$lib/data/deals';
  import { STORES } from '$lib/data/stores';

  // Product stats
  const totalProducts = PRODUCTS.length;
  const totalDeals = DEALS.length;
  const withImages = PRODUCTS.filter(p => p.imageUrl).length;
  const withPrices = PRODUCTS.filter(p => Object.keys(p.prices).length > 0).length;
  const withWeight = PRODUCTS.filter(p => p.size && p.size !== '').length;

  // Category breakdown
  const categories: Record<string, number> = {};
  for (const p of PRODUCTS) {
    categories[p.category] = (categories[p.category] || 0) + 1;
  }
  const sortedCategories = Object.entries(categories).sort((a, b) => b[1] - a[1]);

  // Store coverage
  const storeCoverage: Record<string, number> = {};
  for (const p of PRODUCTS) {
    for (const storeId of Object.keys(p.prices)) {
      storeCoverage[storeId] = (storeCoverage[storeId] || 0) + 1;
    }
  }

  // Price stats
  const allPrices = PRODUCTS.flatMap(p => Object.values(p.prices));
  const avgPrice = allPrices.length > 0 ? (allPrices.reduce((a, b) => a + b, 0) / allPrices.length) : 0;
  const maxPrice = Math.max(...allPrices, 0);
  const minPrice = Math.min(...allPrices.filter(p => p > 0), 0);

  // Deal stats
  const avgDiscount = DEALS.length > 0 ? (DEALS.reduce((a, d) => a + d.discount, 0) / DEALS.length) : 0;
  const maxDiscount = Math.max(...DEALS.map(d => d.discount), 0);

  // Brand breakdown (top 10)
  const brands: Record<string, number> = {};
  for (const p of PRODUCTS) {
    const brand = p.brand || 'Onbekend';
    brands[brand] = (brands[brand] || 0) + 1;
  }
  const topBrands = Object.entries(brands).sort((a, b) => b[1] - a[1]).slice(0, 15);
</script>

<div class="page">
  <h1 class="page-title">Admin Dashboard</h1>
  <p class="subtitle">Scraper status & data quality</p>

  <div class="stats-grid">
    <div class="stat-card">
      <span class="stat-value">{totalProducts}</span>
      <span class="stat-label">Producten</span>
    </div>
    <div class="stat-card accent">
      <span class="stat-value">{totalDeals}</span>
      <span class="stat-label">Deals</span>
    </div>
    <div class="stat-card">
      <span class="stat-value">{Object.keys(storeCoverage).length}</span>
      <span class="stat-label">Winkels actief</span>
    </div>
    <div class="stat-card">
      <span class="stat-value">{Math.round(avgDiscount)}%</span>
      <span class="stat-label">Gem. korting</span>
    </div>
  </div>

  <div class="section-grid">
    <div class="section">
      <h2>Data Quality</h2>
      <div class="quality-bars">
        <div class="quality-row">
          <span class="q-label">Met afbeelding</span>
          <div class="q-bar"><div class="q-fill" style:width="{(withImages / totalProducts * 100)}%"></div></div>
          <span class="q-pct">{Math.round(withImages / totalProducts * 100)}%</span>
        </div>
        <div class="quality-row">
          <span class="q-label">Met prijs</span>
          <div class="q-bar"><div class="q-fill green" style:width="{(withPrices / totalProducts * 100)}%"></div></div>
          <span class="q-pct">{Math.round(withPrices / totalProducts * 100)}%</span>
        </div>
        <div class="quality-row">
          <span class="q-label">Met gewicht/maat</span>
          <div class="q-bar"><div class="q-fill blue" style:width="{(withWeight / totalProducts * 100)}%"></div></div>
          <span class="q-pct">{Math.round(withWeight / totalProducts * 100)}%</span>
        </div>
      </div>
    </div>

    <div class="section">
      <h2>Winkel dekking</h2>
      <div class="store-list">
        {#each STORES as store}
          {@const count = storeCoverage[store.id] || 0}
          <div class="store-row">
            <span class="store-dot" style:background={store.color}></span>
            <span class="store-name">{store.name}</span>
            <span class="store-count">{count > 0 ? `${count} producten` : 'Geen data'}</span>
            <span class="store-status" class:active={count > 0}>{count > 0 ? 'Actief' : 'Wacht'}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <div class="section-grid">
    <div class="section">
      <h2>Categorieën</h2>
      <div class="cat-list">
        {#each sortedCategories as [cat, count]}
          <div class="cat-row">
            <span class="cat-name">{cat}</span>
            <div class="cat-bar"><div class="cat-fill" style:width="{(count / totalProducts * 100)}%"></div></div>
            <span class="cat-count">{count}</span>
          </div>
        {/each}
      </div>
    </div>

    <div class="section">
      <h2>Top Merken</h2>
      <div class="brand-list">
        {#each topBrands as [brand, count]}
          <div class="brand-row">
            <span class="brand-name">{brand}</span>
            <span class="brand-count">{count}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <div class="section">
    <h2>Prijsstatistieken</h2>
    <div class="price-stats">
      <div class="ps-item">
        <span class="ps-value">€{avgPrice.toFixed(2)}</span>
        <span class="ps-label">Gem. prijs</span>
      </div>
      <div class="ps-item">
        <span class="ps-value">€{minPrice.toFixed(2)}</span>
        <span class="ps-label">Laagste</span>
      </div>
      <div class="ps-item">
        <span class="ps-value">€{maxPrice.toFixed(2)}</span>
        <span class="ps-label">Hoogste</span>
      </div>
      <div class="ps-item">
        <span class="ps-value">{maxDiscount}%</span>
        <span class="ps-label">Max korting</span>
      </div>
    </div>
  </div>
</div>

<style>
  .page {
    padding: var(--space-5);
    padding-bottom: 96px;
    display: flex;
    flex-direction: column;
    gap: var(--space-5);
    max-width: 1000px;
    margin: 0 auto;
  }

  .page-title {
    font-size: 28px;
    color: var(--dark);
  }

  .subtitle {
    font-size: 14px;
    color: var(--gray-500);
    margin-top: -12px;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-3);
  }

  .stat-card {
    background: white;
    border: 1px solid var(--gray-200);
    padding: var(--space-5);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-1);
  }

  .stat-card.accent {
    background: var(--orange);
    border-color: var(--orange);
    color: white;
  }

  .stat-value {
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  .stat-label {
    font-size: 13px;
    font-weight: 600;
    opacity: 0.7;
  }

  .section-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-4);
  }

  .section {
    background: white;
    border: 1px solid var(--gray-200);
    padding: var(--space-5);
  }

  .section h2 {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: var(--space-4);
    color: var(--dark);
  }

  .quality-bars {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .quality-row {
    display: flex;
    align-items: center;
    gap: var(--space-3);
  }

  .q-label {
    font-size: 13px;
    font-weight: 600;
    width: 120px;
    flex-shrink: 0;
    color: var(--gray-700);
  }

  .q-bar {
    flex: 1;
    height: 8px;
    background: var(--gray-100);
    border-radius: 4px;
    overflow: hidden;
  }

  .q-fill {
    height: 100%;
    background: var(--orange);
    border-radius: 4px;
    transition: width 0.6s ease;
  }

  .q-fill.green { background: var(--green); }
  .q-fill.blue { background: var(--blue); }

  .q-pct {
    font-size: 13px;
    font-weight: 700;
    width: 40px;
    text-align: right;
    color: var(--dark);
  }

  .store-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
  }

  .store-row {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) 0;
    border-bottom: 1px solid var(--gray-100);
  }

  .store-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .store-name {
    font-size: 14px;
    font-weight: 600;
    flex: 1;
  }

  .store-count {
    font-size: 12px;
    color: var(--gray-500);
  }

  .store-status {
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: var(--radius-full);
    background: var(--gray-100);
    color: var(--gray-500);
  }

  .store-status.active {
    background: var(--green-light);
    color: var(--green-dark);
  }

  .cat-list, .brand-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
  }

  .cat-row {
    display: flex;
    align-items: center;
    gap: var(--space-2);
  }

  .cat-name {
    font-size: 13px;
    font-weight: 600;
    width: 80px;
    flex-shrink: 0;
    color: var(--gray-700);
  }

  .cat-bar {
    flex: 1;
    height: 6px;
    background: var(--gray-100);
    border-radius: 3px;
    overflow: hidden;
  }

  .cat-fill {
    height: 100%;
    background: var(--orange-warm);
    border-radius: 3px;
  }

  .cat-count {
    font-size: 12px;
    font-weight: 700;
    width: 30px;
    text-align: right;
    color: var(--gray-600);
  }

  .brand-row {
    display: flex;
    justify-content: space-between;
    padding: var(--space-1) 0;
    border-bottom: 1px solid var(--gray-100);
  }

  .brand-name {
    font-size: 13px;
    font-weight: 600;
    color: var(--gray-700);
  }

  .brand-count {
    font-size: 13px;
    font-weight: 700;
    color: var(--orange);
  }

  .price-stats {
    display: flex;
    gap: var(--space-6);
  }

  .ps-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .ps-value {
    font-size: 24px;
    font-weight: 700;
    color: var(--green-dark);
  }

  .ps-label {
    font-size: 12px;
    color: var(--gray-500);
    font-weight: 500;
  }

  @media (max-width: 767px) {
    .stats-grid {
      grid-template-columns: 1fr 1fr;
    }
    .section-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
