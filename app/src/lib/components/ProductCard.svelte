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

<div class="product-card">
  <div class="header">
    <span class="dot" style:background={dotColor}></span>
    <div class="title">
      <span class="name">{product.name}</span>
      <span class="meta">{product.brand}{product.brand && product.size ? ' \u2022 ' : ''}{product.size}</span>
    </div>
  </div>

  <div class="badges">
    {#each sortedPrices as [storeId, price], i}
      <StoreBadge
        {storeId}
        {price}
        cheapest={storeId === cheapest[0]}
        duur={storeId === expensive[0]}
      />
    {/each}
  </div>

  <div class="footer">
    <span class="keuze">Oma's Keuze: <strong>{formatPrice(cheapest[1])}</strong></span>
    <button class="add-btn" onclick={addToList}>+ Lijst</button>
  </div>
</div>

<style>
  .product-card {
    background: white;
    border-radius: var(--radius-md);
    padding: var(--space-4);
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    animation: slideUp 0.3s ease-out;
    transition: transform var(--transition-fast), box-shadow var(--transition-fast);
  }

  .product-card:hover {
    box-shadow: var(--shadow-md);
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
    font-size: 12px;
    color: var(--gray-500);
    margin-top: 1px;
  }

  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-1);
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
    background: transparent;
    color: var(--green-dark);
    border: 1.5px solid var(--green);
    border-radius: var(--radius-sm);
    padding: 5px 14px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition-fast);
  }

  .add-btn:hover {
    background: var(--green-light);
  }
</style>
