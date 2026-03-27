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

  const categoryColors: Record<string, string> = {
    zuivel: '#4FC3F7',
    brood: '#FFB74D',
    groente: '#81C784',
    dranken: '#BA68C8'
  };

  let dotColor = $derived(categoryColors[product.category] ?? '#BDBDBD');

  function addToList() {
    shoppingList.add(product.id);
    toasts.show(`${product.name} toegevoegd!`);
  }
</script>

<div class="product-card" style:--cat-color={dotColor}>
  <div class="cat-border"></div>
  <div class="card-body">
    <div class="header">
      <span class="dot" style:background={dotColor}></span>
      <div class="title">
        <span class="name">{product.name}</span>
        <span class="meta">{product.brand}{product.brand && product.size ? ' \u2022 ' : ''}{product.size}</span>
      </div>
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
      <span class="keuze">Oma's Keuze: <strong>{formatPrice(cheapest[1])}</strong></span>
      <button class="add-btn" onclick={addToList}>+ Lijst</button>
    </div>
  </div>
</div>

<style>
  .product-card {
    background: white;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    display: flex;
    overflow: hidden;
    animation: slideUp 0.3s ease-out;
    transition: transform var(--transition-fast), box-shadow var(--transition-fast);
  }

  .product-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
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
    gap: var(--space-3);
  }

  .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 5px;
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
    justify-content: space-between;
    padding-top: var(--space-2);
    border-top: 1px solid var(--gray-100);
  }

  .keuze {
    font-size: 13px;
    color: var(--green-dark);
    font-weight: 500;
  }

  .keuze strong {
    font-weight: 700;
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
    transition: all var(--transition-fast);
    box-shadow: 0 2px 8px rgba(0, 200, 83, 0.2);
  }

  .add-btn:hover {
    background: var(--green-dark);
    transform: translateY(-1px);
    box-shadow: var(--shadow-green);
  }

  .add-btn:active {
    transform: scale(0.96);
  }
</style>
