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
    <label class="checkbox-target">
    <button class="checkbox" class:is-checked={checked} onclick={ontoggle}>
      {#if checked}
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M2.5 7L5.5 10L11.5 4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="20"/>
        </svg>
      {/if}
    </button>
    </label>
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
    padding: 14px var(--space-4) 14px 0;
    transition: opacity var(--transition-base);
    overflow: hidden;
    border-bottom: 1px solid #F0F0F0;
  }


  .list-item.checked {
    opacity: 0.35;
    transition: opacity 0.4s ease;
  }

  .list-item.checked .name {
    text-decoration: line-through;
    color: var(--gray-500);
    transition: color 0.3s ease;
  }

  .checkbox-target {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    flex-shrink: 0;
    cursor: pointer;
  }

  .checkbox {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 2px solid var(--gray-300);
    background: white;
    cursor: pointer;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .checkbox.is-checked {
    background: var(--orange);
    border-color: var(--orange);
    box-shadow: 0 2px 6px rgba(255, 98, 0, 0.25);
    animation: checkPop 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .checkbox.is-checked svg {
    animation: checkDraw 0.3s ease-out 0.05s both;
  }

  @keyframes checkPop {
    0% { transform: scale(0.7); }
    50% { transform: scale(1.15); }
    100% { transform: scale(1); }
  }

  @keyframes checkDraw {
    from { stroke-dashoffset: 20; opacity: 0; }
    to { stroke-dashoffset: 0; opacity: 1; }
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
    font-weight: 700;
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
    padding: 14px;
    border-radius: 50%;
    transition: all var(--transition-fast);
    display: flex;
    align-items: center;
  }

  .remove:hover {
    color: var(--red);
    background: var(--red-light);
  }
</style>
