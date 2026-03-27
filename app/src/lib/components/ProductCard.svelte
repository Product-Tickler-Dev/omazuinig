<script lang="ts">
  import type { Product } from '$lib/data/types';
  import { getCheapestStore, getMostExpensiveStore, formatPrice } from '$lib/utils/price';
  import { getCategoryColor } from '$lib/data/categories';
  import StoreBadge from './StoreBadge.svelte';
  import { shoppingList } from '$lib/stores/shoppingList';
  import { toasts } from '$lib/stores/toast';

  let { product }: { product: Product } = $props();

  let cheapest = $derived(getCheapestStore(product));
  let expensive = $derived(getMostExpensiveStore(product));
  let sortedPrices = $derived(
    Object.entries(product.prices).sort((a, b) => a[1] - b[1])
  );

  let catColor = $derived(getCategoryColor(product.category));

  function addToList() {
    shoppingList.add(product.id);
    toasts.show(`${product.name} toegevoegd!`);
  }
</script>

<div class="product-card" style:--cat-color={catColor}>
  <div class="cat-border"></div>
  <div class="card-body">
    <div class="header">
      <div class="title">
        <span class="name">{product.name}</span>
        <span class="meta">{product.brand}{product.brand && product.size ? ' \u2022 ' : ''}{product.size}</span>
      </div>
      <span class="cat-label">{product.category}</span>
    </div>

    <div class="badges">
      {#each sortedPrices.slice(0, 4) as [storeId, price], i}
        <StoreBadge
          {storeId}
          {price}
          cheapest={storeId === cheapest[0]}
          duur={false}
        />
      {/each}
      {#if sortedPrices.length > 4}
        <span class="more-stores">+{sortedPrices.length - 4}</span>
      {/if}
    </div>

    <div class="footer">
      <button class="add-btn" onclick={addToList}>+ Lijst</button>
    </div>
  </div>
</div>

<style>
  .product-card {
    display: flex;
    overflow: hidden;
    border-bottom: 1px solid #F0F0F0;
  }

  .cat-border {
    width: 3px;
    flex-shrink: 0;
    background: var(--cat-color);
  }

  .card-body {
    flex: 1;
    min-width: 0;
    padding: var(--space-3) var(--space-4);
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
  }

  .header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: var(--space-3);
  }

  .cat-label {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--gray-500);
    flex-shrink: 0;
    margin-top: 3px;
  }

  .title {
    display: flex;
    flex-direction: column;
  }

  .name {
    font-weight: 700;
    font-size: 15px;
    line-height: 1.3;
  }

  .meta {
    font-size: 13px;
    color: var(--gray-500);
    margin-top: 1px;
  }

  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-1);
    align-items: center;
  }

  .more-stores {
    font-size: 11px;
    color: var(--gray-500);
    font-weight: 500;
    padding: 2px 6px;
  }

  .footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-top: var(--space-2);
    border-top: 1px solid var(--gray-100);
  }

  .add-btn {
    background: var(--green);
    color: white;
    border: none;
    border-radius: var(--radius-full);
    padding: 7px 16px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: background var(--transition-fast);
  }

  .add-btn:hover {
    background: var(--green-dark);
  }

  .add-btn:active {
    opacity: 0.85;
  }
</style>
