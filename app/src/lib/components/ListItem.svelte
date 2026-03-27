<script lang="ts">
  import { getProduct } from '$lib/data/products';
  import { getCheapestStore } from '$lib/utils/price';
  import StoreBadge from './StoreBadge.svelte';

  let { productId, checked, ontoggle, onremove }: {
    productId: number;
    checked: boolean;
    ontoggle: () => void;
    onremove: () => void;
  } = $props();

  let product = $derived(getProduct(productId));
  let sortedPrices = $derived(
    product ? Object.entries(product.prices).sort((a, b) => a[1] - b[1]).slice(0, 4) : []
  );
  let cheapestId = $derived(product ? getCheapestStore(product)[0] : '');
</script>

{#if product}
  <div class="list-item" class:checked>
    <button class="checkbox" onclick={ontoggle}>
      {#if checked}
        &#x2705;
      {:else}
        &#x2B1C;
      {/if}
    </button>
    <span class="emoji">{product.image}</span>
    <div class="info">
      <span class="name">{product.name}</span>
      <span class="size">{product.size}</span>
      <div class="badges">
        {#each sortedPrices as [storeId, price]}
          <StoreBadge {storeId} {price} cheapest={storeId === cheapestId} />
        {/each}
      </div>
    </div>
    <button class="remove" onclick={onremove}>&#x2716;</button>
  </div>
{/if}

<style>
  .list-item {
    display: flex;
    align-items: center;
    gap: 10px;
    background: white;
    border-radius: var(--radius-md);
    padding: 12px;
    box-shadow: var(--shadow-sm);
    animation: slideUp 0.3s ease-out;
  }

  .list-item.checked {
    opacity: 0.5;
  }

  .list-item.checked .name,
  .list-item.checked .size {
    text-decoration: line-through;
  }

  .checkbox {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    flex-shrink: 0;
    padding: 0;
  }

  .emoji {
    font-size: 28px;
    flex-shrink: 0;
  }

  .info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .name {
    font-weight: 700;
    font-size: 14px;
  }

  .size {
    font-size: 12px;
    color: #888;
  }

  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-top: 4px;
  }

  .remove {
    background: none;
    border: none;
    font-size: 16px;
    cursor: pointer;
    color: var(--red);
    flex-shrink: 0;
    padding: 4px;
  }
</style>
