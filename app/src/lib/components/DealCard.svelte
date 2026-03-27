<script lang="ts">
  import type { Deal } from '$lib/data/types';
  import { getProduct } from '$lib/data/products';
  import { getStore } from '$lib/data/stores';
  import { formatPrice } from '$lib/utils/price';

  let { deal }: { deal: Deal } = $props();

  let product = $derived(getProduct(deal.productId));
  let store = $derived(getStore(deal.store));

  const categoryColors: Record<string, string> = {
    zuivel: '#4FC3F7',
    brood: '#FFB74D',
    groente: '#81C784',
    dranken: '#BA68C8'
  };

  let dotColor = $derived(product ? categoryColors[product.category] ?? '#BDBDBD' : '#BDBDBD');
</script>

{#if product && store}
  <div class="deal-card">
    <div class="store-stripe" style:background={store.color}></div>
    <div class="card-body">
      <div class="card-top">
        <span class="store-name" style:color={store.color}>{store.name}</span>
        <span class="discount-badge">-{deal.discount}%</span>
      </div>
      <div class="product-info">
        <span class="dot" style:background={dotColor}></span>
        <div class="product-text">
          <span class="product-name">{product.name}</span>
          <span class="product-meta">{product.brand}{product.brand && product.size ? ' \u2022 ' : ''}{product.size}</span>
        </div>
      </div>
      <div class="price-row">
        <div class="prices">
          <span class="old-price">{formatPrice(deal.oldPrice)}</span>
          <span class="new-price">{formatPrice(deal.newPrice)}</span>
        </div>
        {#if deal.discount >= 40}
          <span class="hamster-pill">Hamsteralert</span>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .deal-card {
    background: white;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    min-height: 140px;
    overflow: hidden;
    transition: transform var(--transition-fast), box-shadow var(--transition-fast);
    animation: bounceIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .deal-card:hover {
    transform: scale(1.02);
    box-shadow: var(--shadow-md);
  }

  .deal-card:active {
    transform: scale(0.99);
  }

  .store-stripe {
    height: 4px;
    width: 100%;
    flex-shrink: 0;
  }

  .card-body {
    padding: var(--space-4);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    flex: 1;
  }

  .card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .store-name {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
  }

  .discount-badge {
    background: var(--orange);
    color: white;
    font-size: 12px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: var(--radius-full);
    box-shadow: 0 2px 8px rgba(255, 98, 0, 0.2);
  }

  .product-info {
    display: flex;
    align-items: flex-start;
    gap: var(--space-2);
  }

  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 7px;
  }

  .product-text {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }

  .product-name {
    font-weight: 700;
    font-size: 16px;
    line-height: 1.3;
  }

  .product-meta {
    font-size: 13px;
    color: var(--gray-500);
    margin-top: 1px;
  }

  .price-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: auto;
  }

  .prices {
    display: flex;
    align-items: baseline;
    gap: var(--space-2);
  }

  .old-price {
    color: var(--gray-400);
    text-decoration: line-through;
    font-size: 13px;
  }

  .new-price {
    color: var(--green-dark);
    font-weight: 700;
    font-size: 24px;
    letter-spacing: -0.02em;
  }

  .hamster-pill {
    background: linear-gradient(135deg, var(--orange) 0%, var(--orange-warm, #FF8A3D) 100%);
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: var(--radius-full);
    white-space: nowrap;
    animation: subtlePulse 2s ease-in-out infinite;
    box-shadow: 0 2px 8px rgba(255, 98, 0, 0.2);
  }
</style>
