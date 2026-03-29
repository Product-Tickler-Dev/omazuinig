<script lang="ts">
  import type { Product } from '$lib/data/types';
  import { getCheapestStore, getMostExpensiveStore, formatPrice } from '$lib/utils/price';
  import StoreBadge from './StoreBadge.svelte';
  import { shoppingList } from '$lib/stores/shoppingList';
  import { toasts } from '$lib/stores/toast';

  let { product }: { product: Product } = $props();

  let cheapest = $derived(getCheapestStore(product));
  let expensive = $derived(getMostExpensiveStore(product));
  let sortedPrices = $derived(
    Object.entries(product.prices).sort((a, b) => a[1] - b[1])
  );

  function addToList() {
    shoppingList.add(product.id);
    const savings = expensive[1] - cheapest[1];
    if (savings > 0) {
      toasts.celebrate(`Toegevoegd!`, savings);
    } else {
      toasts.show(`${product.name} toegevoegd!`);
    }
  }
</script>

<div class="product-card">
  <div class="card-body">
    <div class="header">
      {#if product.imageUrl}
        <img src={product.imageUrl} alt="" class="product-img" loading="lazy" />
      {/if}
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
    transition: background 0.15s ease, box-shadow 0.2s ease;
  }

  @media (min-width: 768px) {
    .product-card:hover {
      background: var(--gray-50);
    }
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

  .product-img {
    width: 48px;
    height: 48px;
    object-fit: contain;
    flex-shrink: 0;
    border-radius: var(--radius-sm);
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
    transition: background var(--transition-fast), transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease;
  }

  .add-btn:hover {
    background: var(--green-dark);
    box-shadow: var(--shadow-green);
  }

  .add-btn:active {
    transform: scale(0.9);
  }
</style>
