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
  let bgColor = $derived(cheapest ? 'var(--green)' : duur ? 'var(--red)' : store?.color ?? '#888');
</script>

<span
  class="badge"
  class:cheapest
  class:duur
  style:background-color={bgColor}
>
  <span class="name">{store?.short ?? storeId}</span>
  <span class="price" class:strikethrough={duur}>{formatPrice(price)}</span>
</span>

<style>
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    color: white;
    white-space: nowrap;
  }

  .badge.duur {
    opacity: 0.7;
  }

  .name {
    font-size: 11px;
  }

  .strikethrough {
    text-decoration: line-through;
  }
</style>
