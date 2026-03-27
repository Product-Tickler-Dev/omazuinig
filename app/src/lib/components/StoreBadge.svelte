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

<span
  class="badge"
  class:cheapest
  class:duur
  class:default={!cheapest && !duur}
  style:--store-color={store?.color ?? '#888'}
>
  <span class="name">{store?.short ?? storeId}</span>
  <span class="price" class:strikethrough={duur}>{formatPrice(price)}</span>
</span>

<style>
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    padding: 3px 7px;
    border-radius: var(--radius-full);
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
    transition: all var(--transition-fast);
  }

  .badge.cheapest {
    background: var(--green-light);
    color: var(--green-dark);
  }

  .badge.duur {
    background: var(--gray-100);
    color: var(--gray-500);
  }

  .badge.default {
    background: var(--gray-100);
    color: var(--store-color);
  }

  .name {
    font-size: 10px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.02em;
  }

  .price {
    font-weight: 700;
    font-size: 12px;
  }

  .strikethrough {
    text-decoration: line-through;
    color: var(--gray-400);
  }
</style>
