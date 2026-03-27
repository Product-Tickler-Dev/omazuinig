<script lang="ts">
  import type { Deal } from '$lib/data/types';
  import { getProduct } from '$lib/data/products';
  import { getStore } from '$lib/data/stores';
  import { formatPrice } from '$lib/utils/price';

  let { deal }: { deal: Deal } = $props();

  let product = $derived(getProduct(deal.productId));
  let store = $derived(getStore(deal.store));
</script>

{#if product && store}
  <div class="deal-card">
    <div class="emoji">{product.image}</div>
    <div class="info">
      <div class="top-row">
        <span class="product-name">{product.name}</span>
        {#if deal.discount >= 40}
          <span class="hamster-badge">&#x1F439; Hamsteralert!</span>
        {/if}
      </div>
      <span class="store-name" style:color={store.color}>{store.name}</span>
      <div class="price-row">
        <span class="old-price">{formatPrice(deal.oldPrice)}</span>
        <span class="new-price">{formatPrice(deal.newPrice)}</span>
        <span class="discount-badge">-{deal.discount}%</span>
      </div>
    </div>
  </div>
{/if}

<style>
  .deal-card {
    display: flex;
    align-items: center;
    gap: 12px;
    background: white;
    border-radius: var(--radius-md);
    padding: 12px;
    box-shadow: var(--shadow-sm);
    animation: slideUp 0.3s ease-out;
  }

  .emoji {
    font-size: 36px;
    flex-shrink: 0;
  }

  .info {
    flex: 1;
    min-width: 0;
  }

  .top-row {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }

  .product-name {
    font-weight: 700;
    font-size: 15px;
  }

  .hamster-badge {
    background: var(--orange);
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 999px;
  }

  .store-name {
    font-size: 13px;
    font-weight: 700;
  }

  .price-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 4px;
  }

  .old-price {
    color: var(--red);
    text-decoration: line-through;
    font-size: 14px;
  }

  .new-price {
    color: var(--green);
    font-weight: 700;
    font-size: 16px;
  }

  .discount-badge {
    background: var(--orange);
    color: white;
    font-size: 12px;
    font-weight: 700;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
