<script lang="ts">
  import { PRODUCTS } from '$lib/data/products';
  import ProductCard from '$lib/components/ProductCard.svelte';
  import CategoryPills from '$lib/components/CategoryPills.svelte';
  import OmaBubble from '$lib/components/OmaBubble.svelte';

  const categories = ['alles', 'zuivel', 'brood', 'groente', 'dranken'];

  let activeCategory = $state('alles');
  let searchQuery = $state('');

  let filteredProducts = $derived(
    PRODUCTS.filter(p => {
      const matchesCategory = activeCategory === 'alles' || p.category === activeCategory;
      const matchesSearch = searchQuery.length === 0 || p.name.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    })
  );
</script>

<div class="page">
  <header class="top-bar">
    <h1>Vergelijk</h1>
  </header>

  <div class="search-box">
    <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="11" cy="11" r="8"/>
      <path d="M21 21l-4.35-4.35"/>
    </svg>
    <input
      type="text"
      class="search-input"
      placeholder="Zoek een product..."
      bind:value={searchQuery}
    />
  </div>

  <CategoryPills
    {categories}
    active={activeCategory}
    onselect={(cat) => activeCategory = cat}
  />

  {#if filteredProducts.length === 0}
    <OmaBubble text="Niks gevonden. Probeer iets anders!" />
  {:else}
    <div class="product-list">
      {#each filteredProducts as product (product.id)}
        <ProductCard {product} />
      {/each}
    </div>
  {/if}
</div>

<style>
  .page {
    padding: var(--space-4);
    padding-bottom: 88px;
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    overflow-x: hidden;
  }

  .top-bar {
    padding: var(--space-1) 0;
  }

  .top-bar h1 {
    font-size: 22px;
  }

  .search-box {
    position: relative;
    display: flex;
    align-items: center;
  }

  .search-icon {
    position: absolute;
    left: 14px;
    color: var(--gray-400);
    pointer-events: none;
  }

  .search-input {
    width: 100%;
    padding: var(--space-3) var(--space-4) var(--space-3) 42px;
    border: 1.5px solid var(--gray-200);
    border-radius: var(--radius-md);
    font-size: 15px;
    font-family: inherit;
    background: white;
    outline: none;
    transition: border-color var(--transition-fast);
    color: var(--dark);
  }

  .search-input:focus {
    border-color: var(--orange);
  }

  .product-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }
</style>
