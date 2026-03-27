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
  <div class="search-box">
    <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
    <div class="empty-state">
      <OmaBubble text="Niks gevonden, lieverd. Probeer iets anders!" />
    </div>
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
    padding: var(--space-5);
    padding-bottom: 96px;
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
    overflow-x: hidden;
  }

  .search-box {
    position: relative;
    display: flex;
    align-items: center;
  }

  .search-icon {
    position: absolute;
    left: 18px;
    color: var(--gray-400);
    pointer-events: none;
  }

  .search-input {
    width: 100%;
    height: 56px;
    padding: 0 var(--space-4) 0 52px;
    border: 2px solid var(--gray-200);
    border-radius: var(--radius-lg);
    font-size: 16px;
    font-family: inherit;
    background: white;
    outline: none;
    transition: all var(--transition-fast);
    color: var(--dark);
  }

  .search-input:focus {
    border-color: var(--orange);
    box-shadow: 0 0 0 3px rgba(255, 98, 0, 0.08);
  }

  .empty-state {
    padding: var(--space-8) 0;
  }

  .product-list {
    display: flex;
    flex-direction: column;
  }
</style>
