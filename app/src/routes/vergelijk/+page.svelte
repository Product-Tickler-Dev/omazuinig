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
    <h1>&#x1F50D; Vergelijk</h1>
  </header>

  <input
    type="text"
    class="search-input"
    placeholder="Zoek een product..."
    bind:value={searchQuery}
  />

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
    padding: 16px;
    padding-bottom: 80px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .top-bar {
    padding: 4px 0;
  }

  .top-bar h1 {
    font-size: 22px;
  }

  .search-input {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #e0e0e0;
    border-radius: var(--radius-md);
    font-size: 15px;
    font-family: inherit;
    background: white;
    outline: none;
    transition: border-color 0.2s;
  }

  .search-input:focus {
    border-color: var(--orange);
  }

  .product-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
</style>
