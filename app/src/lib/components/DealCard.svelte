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
{/if}

<style>
  .deal-card {
    background: white;
    border-radius: var(--radius-md);
    padding: var(--space-4);
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    min-height: 130px;
    transition: transform var(--transition-fast), box-shadow var(--transition-fast);
    animation: slideUp 0.3s ease-out;
  }

  .deal-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  .card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .store-name {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.02em;
  }

  .discount-badge {
    background: var(--orange);
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: var(--radius-full);
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
    margin-top: 6px;
  }

  .product-text {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }

  .product-name {
    font-weight: 700;
    font-size: 14px;
    line-height: 1.3;
  }

  .product-meta {
    font-size: 12px;
    color: var(--gray-500);
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
    font-size: 20px;
  }

  .hamster-pill {
    background: var(--orange-light);
    color: var(--orange);
    font-size: 10px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: var(--radius-full);
    white-space: nowrap;
  }
</style>
