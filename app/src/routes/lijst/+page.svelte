<script lang="ts">
  import { shoppingList } from '$lib/stores/shoppingList';
  import { PRODUCTS, getProduct } from '$lib/data/products';
  import { getStore } from '$lib/data/stores';
  import ListItem from '$lib/components/ListItem.svelte';
  import OmaBubble from '$lib/components/OmaBubble.svelte';
  import { formatPrice, getCheapestStore, calculateSplitSavings, calculateBestSingleStore } from '$lib/utils/price';
  import { toasts } from '$lib/stores/toast';

  let searchQuery = $state('');
  let adviceMode = $state<'single' | 'split'>('single');

  let items = $derived($shoppingList);
  let uncheckedItems = $derived(items.filter(i => !i.checked));
  let checkedItems = $derived(items.filter(i => i.checked));
  let sortedItems = $derived([...uncheckedItems, ...checkedItems]);

  let searchResults = $derived(
    searchQuery.length > 0
      ? PRODUCTS
          .filter(p => p.name.toLowerCase().includes(searchQuery.toLowerCase()))
          .filter(p => !items.find(i => i.productId === p.id))
          .slice(0, 5)
      : []
  );

  let bestSingleStore = $derived(calculateBestSingleStore(items, getProduct));
  let cheapestStoreEntry = $derived(bestSingleStore[0]);
  let cheapestStoreName = $derived(
    cheapestStoreEntry ? getStore(cheapestStoreEntry[0])?.name ?? '' : ''
  );
  let cheapestStoreTotal = $derived(cheapestStoreEntry ? cheapestStoreEntry[1] : 0);

  let splitResult = $derived(calculateSplitSavings(items, getProduct));
  let splitStoreNames = $derived(
    splitResult.storesUsed.map(id => getStore(id)?.name ?? id).join(', ')
  );

  function addItem(productId: number) {
    shoppingList.add(productId);
    const product = getProduct(productId);
    toasts.show(`${product?.name ?? 'Product'} toegevoegd!`);
    searchQuery = '';
  }
</script>

<div class="page">
  <header class="top-bar">
    <h1>&#x1F4CB; Boodschappenlijst</h1>
    {#if items.length > 0}
      <span class="count-badge">{items.length}</span>
    {/if}
  </header>

  <div class="search-wrapper">
    <input
      type="text"
      class="search-input"
      placeholder="Voeg product toe..."
      bind:value={searchQuery}
    />
    {#if searchResults.length > 0}
      <div class="autocomplete">
        {#each searchResults as product}
          <button class="autocomplete-item" onclick={() => addItem(product.id)}>
            <span class="ac-emoji">{product.image}</span>
            <span class="ac-name">{product.name}</span>
            <span class="ac-size">{product.size}</span>
          </button>
        {/each}
      </div>
    {/if}
  </div>

  {#if items.length === 0}
    <OmaBubble text="Je lijst is leeg! Voeg iets toe, lieverd." />
  {:else}
    <div class="list">
      {#each sortedItems as item (item.productId)}
        <ListItem
          productId={item.productId}
          checked={item.checked}
          ontoggle={() => shoppingList.toggle(item.productId)}
          onremove={() => shoppingList.remove(item.productId)}
        />
      {/each}
    </div>

    <div class="advice-panel">
      <div class="advice-header">
        <span class="advice-avatar">&#x1F475;</span>
        <strong>Oma's Advies</strong>
      </div>
      <div class="mode-toggle">
        <button
          class="mode-btn"
          class:active={adviceMode === 'single'}
          onclick={() => adviceMode = 'single'}
        >&#x1F3EA; E&eacute;n winkel</button>
        <button
          class="mode-btn"
          class:active={adviceMode === 'split'}
          onclick={() => adviceMode = 'split'}
        >&#x1F4B0; Max besparing</button>
      </div>
      <div class="advice-text">
        {#if adviceMode === 'single'}
          <p>Ga naar <strong>{cheapestStoreName}</strong> &mdash; totaal {formatPrice(cheapestStoreTotal)}</p>
        {:else}
          <p><strong>{splitStoreNames}</strong> = {formatPrice(splitResult.splitTotal)} &mdash; besparing {formatPrice(splitResult.savings)}!</p>
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
  .page {
    padding: 16px;
    padding-bottom: 200px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .top-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 4px 0;
  }

  .top-bar h1 {
    font-size: 22px;
  }

  .count-badge {
    background: var(--orange);
    color: white;
    font-size: 13px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 999px;
  }

  .search-wrapper {
    position: relative;
  }

  .search-input {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #e0e0e0;
    border-radius: var(--radius-md);
    font-size: 15px;
    font-family: inherit;
    background: white;
    outline: none;
    transition: border-color 0.2s;
  }

  .search-input:focus {
    border-color: var(--orange);
  }

  .autocomplete {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border-radius: 0 0 var(--radius-md) var(--radius-md);
    box-shadow: var(--shadow-md);
    z-index: 10;
    overflow: hidden;
  }

  .autocomplete-item {
    display: flex;
    align-items: center;
    gap: 10px;
    width: 100%;
    padding: 10px 16px;
    border: none;
    background: none;
    cursor: pointer;
    font-family: inherit;
    font-size: 14px;
    text-align: left;
    transition: background 0.15s;
  }

  .autocomplete-item:hover {
    background: var(--cream);
  }

  .ac-emoji {
    font-size: 22px;
  }

  .ac-name {
    font-weight: 700;
    flex: 1;
  }

  .ac-size {
    color: #888;
    font-size: 12px;
  }

  .list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .advice-panel {
    position: sticky;
    bottom: 68px;
    background: white;
    border-radius: var(--radius-lg);
    padding: 16px;
    box-shadow: var(--shadow-lg);
    display: flex;
    flex-direction: column;
    gap: 10px;
    border: 2px solid var(--orange);
  }

  .advice-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
  }

  .advice-avatar {
    font-size: 28px;
  }

  .mode-toggle {
    display: flex;
    gap: 8px;
  }

  .mode-btn {
    flex: 1;
    padding: 8px 12px;
    border: 2px solid var(--orange);
    border-radius: var(--radius-sm);
    background: white;
    font-size: 13px;
    font-weight: 700;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s;
  }

  .mode-btn.active {
    background: var(--orange);
    color: white;
  }

  .advice-text {
    font-size: 14px;
    line-height: 1.5;
  }

  .advice-text strong {
    color: var(--orange);
  }
</style>
