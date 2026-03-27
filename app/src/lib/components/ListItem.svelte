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
    product ? Object.entries(product.prices).sort((a, b) => a[1] - b[1]).slice(0, 3) : []
  );
  let cheapestId = $derived(product ? getCheapestStore(product)[0] : '');
</script>

{#if product}
  <div class="list-item" class:checked>
    <button class="checkbox" class:is-checked={checked} onclick={ontoggle}>
      {#if checked}
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M2.5 7L5.5 10L11.5 4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      {/if}
    </button>
    <div class="info">
      <div class="name-row">
        <span class="name">{product.name}</span>
        <span class="size">{product.size}</span>
      </div>
      <div class="badges">
        {#each sortedPrices as [storeId, price]}
          <StoreBadge {storeId} {price} cheapest={storeId === cheapestId} />
        {/each}
      </div>
    </div>
    <button class="remove" aria-label="Verwijder product" onclick={onremove}>
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
        <path d="M4 4l8 8M12 4l-8 8"/>
      </svg>
    </button>
  </div>
{/if}

<style>
  .list-item {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    background: white;
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-4);
    box-shadow: var(--shadow-xs);
    animation: slideUp 0.3s ease-out;
    transition: opacity var(--transition-base);
  }

  .list-item.checked {
    opacity: 0.4;
  }

  .list-item.checked .name {
    text-decoration: line-through;
    color: var(--gray-500);
  }

  .checkbox {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid var(--gray-300);
    background: white;
    cursor: pointer;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    transition: all var(--transition-fast);
  }

  .checkbox.is-checked {
    background: var(--orange);
    border-color: var(--orange);
  }

  .info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
  }

  .name-row {
    display: flex;
    align-items: baseline;
    gap: var(--space-2);
    flex-wrap: wrap;
  }

  .name {
    font-weight: 600;
    font-size: 14px;
    transition: all var(--transition-base);
  }

  .size {
    font-size: 12px;
    color: var(--gray-500);
  }

  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 3px;
  }

  .remove {
    background: none;
    border: none;
    cursor: pointer;
    color: var(--gray-300);
    flex-shrink: 0;
    padding: 4px;
    border-radius: 4px;
    transition: color var(--transition-fast);
    display: flex;
    align-items: center;
  }

  .remove:hover {
    color: var(--red);
  }
</style>
