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
    toasts.show(`${product.name} toegevoegd!`);
  }
</script>

<div class="product-card">
  <div class="header">
    <span class="emoji">{product.image}</span>
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
    <span class="keuze">&#x1F475; Oma's Keuze: <strong>{formatPrice(cheapest[1])}</strong></span>
    <button class="add-btn" onclick={addToList}>+ Lijst</button>
  </div>
</div>

<style>
  .product-card {
    background: white;
    border-radius: var(--radius-md);
    padding: 14px;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    gap: 10px;
    animation: slideUp 0.3s ease-out;
  }

  .header {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .emoji {
    font-size: 32px;
    flex-shrink: 0;
  }

  .title {
    display: flex;
    flex-direction: column;
  }

  .name {
    font-weight: 700;
    font-size: 15px;
  }

  .meta {
    font-size: 12px;
    color: #888;
  }

  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }

  .footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .keuze {
    font-size: 13px;
    color: var(--dark);
  }

  .add-btn {
    background: var(--green);
    color: white;
    border: none;
    border-radius: var(--radius-sm);
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: opacity 0.2s;
  }

  .add-btn:hover {
    opacity: 0.85;
  }
</style>
