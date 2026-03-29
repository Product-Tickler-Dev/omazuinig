<script lang="ts">
  import type { Deal } from '$lib/data/types';
  import { getProduct } from '$lib/data/products';
  import { getStore } from '$lib/data/stores';
  import { formatPrice } from '$lib/utils/price';
  import { getCategoryColor } from '$lib/data/categories';

  let { deal }: { deal: Deal } = $props();

  let product = $derived(getProduct(deal.productId));
  let store = $derived(getStore(deal.store));

  let dotColor = $derived(product ? getCategoryColor(product.category) : '#BDBDBD');
</script>

{#if product && store}
  <div class="deal-card">
    <div class="card-body">
      <div class="card-top">
        <span class="store-name" style:color={store.color}>{store.name}</span>
        <span class="discount-badge">-{deal.discount}%</span>
      </div>
      <div class="product-info">
        {#if product.imageUrl}
          <img src={product.imageUrl} alt="" class="deal-img" loading="lazy" onerror={(e) => e.currentTarget.style.display = 'none'} />
        {/if}
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
    border: 1px solid #E8E8E8;
    display: flex;
    flex-direction: column;
    min-height: 140px;
    overflow: hidden;
    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), border-color var(--transition-fast), box-shadow 0.2s ease;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
  }

  @media (min-width: 768px) {
    .deal-card:hover {
      transform: translateY(-2px);
      border-color: var(--gray-300);
      box-shadow: var(--shadow-md);
    }
  }

  .deal-card:active {
    transform: scale(0.97);
  }

  .deal-card:active .new-price {
    animation: pricePulse 0.3s ease-out;
  }

  @keyframes pricePulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.12); }
    100% { transform: scale(1); }
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
  }

  .product-info {
    display: flex;
    align-items: flex-start;
    gap: var(--space-3);
  }

  .deal-img {
    width: 56px;
    height: 56px;
    object-fit: contain;
    flex-shrink: 0;
    border-radius: var(--radius-sm);
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
  }
</style>
