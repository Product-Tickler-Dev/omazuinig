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

  const categoryColors: Record<string, string> = {
    zuivel: '#4FC3F7',
    brood: '#FFB74D',
    groente: '#81C784',
    dranken: '#BA68C8'
  };

  let catColor = $derived(product ? categoryColors[product.category] ?? '#BDBDBD' : '#BDBDBD');
</script>

{#if product}
  <div class="list-item" class:checked style:--cat-color={catColor}>
    <div class="cat-accent"></div>
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
    padding: 14px var(--space-4) 14px 0;
    box-shadow: var(--shadow-xs);
    animation: slideUp 0.3s ease-out;
    transition: opacity var(--transition-base);
    overflow: hidden;
    border-bottom: 1px solid var(--gray-100);
  }

  .cat-accent {
    width: 3px;
    align-self: stretch;
    background: var(--cat-color);
    flex-shrink: 0;
    border-radius: 0 2px 2px 0;
  }

  .list-item.checked {
    opacity: 0.35;
  }

  .list-item.checked .name {
    text-decoration: line-through;
    color: var(--gray-500);
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
    transition: all var(--transition-fast);
  }

  .checkbox.is-checked {
    background: var(--orange);
    border-color: var(--orange);
    box-shadow: 0 2px 6px rgba(255, 98, 0, 0.25);
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
    padding: 6px;
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
