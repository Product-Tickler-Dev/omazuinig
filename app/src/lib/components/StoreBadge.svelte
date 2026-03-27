<script lang="ts">
  import { getStore } from '$lib/data/stores';
  import { formatPrice } from '$lib/utils/price';

  let { storeId, price, cheapest = false, duur = false }: {
    storeId: string;
    price: number;
    cheapest?: boolean;
    duur?: boolean;
  } = $props();

  let store = $derived(getStore(storeId));
</script>

{#if !duur}
  <span
    class="badge"
    class:cheapest
    class:default={!cheapest}
  >
    <span class="name">{store?.short ?? storeId}</span>
    <span class="price">{formatPrice(price)}</span>
  </span>
{:else}
  <span class="badge faded">
    <span class="name">{store?.short ?? storeId}</span>
    <span class="price">{formatPrice(price)}</span>
  </span>
{/if}

<style>
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    border-radius: var(--radius-full);
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
    transition: all var(--transition-fast);
  }

  .badge.cheapest {
    background: var(--green-light);
    color: var(--green-dark);
    font-size: 13px;
    padding: 4px 10px;
  }

  .badge.cheapest .price {
    font-size: 13px;
    font-weight: 700;
  }

  .badge.default {
    background: var(--gray-100);
    color: var(--gray-700);
  }

  .badge.faded {
    background: transparent;
    color: var(--gray-400);
    opacity: 0.5;
    font-size: 11px;
    padding: 3px 6px;
  }

  .badge.faded .price {
    text-decoration: line-through;
    font-size: 11px;
  }

  .name {
    font-size: 9px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  .price {
    font-weight: 700;
    font-size: 12px;
  }
</style>
