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
    <h1>Boodschappenlijst</h1>
    {#if items.length > 0}
      <span class="count-badge">{items.length}</span>
    {/if}
  </header>

  <div class="search-wrapper">
    <div class="search-box">
      <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"/>
        <path d="M21 21l-4.35-4.35"/>
      </svg>
      <input
        type="text"
        class="search-input"
        placeholder="Voeg product toe..."
        bind:value={searchQuery}
      />
    </div>
    {#if searchResults.length > 0}
      <div class="autocomplete">
        {#each searchResults as product}
          <button class="autocomplete-item" onclick={() => addItem(product.id)}>
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
        <strong>Oma's Advies</strong>
      </div>
      <div class="mode-toggle">
        <button
          class="mode-btn"
          class:active={adviceMode === 'single'}
          onclick={() => adviceMode = 'single'}
        >E&eacute;n winkel</button>
        <button
          class="mode-btn"
          class:active={adviceMode === 'split'}
          onclick={() => adviceMode = 'split'}
        >Max besparing</button>
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
    padding: var(--space-4);
    padding-bottom: 200px;
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
    overflow-x: hidden;
  }

  .top-bar {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-1) 0;
  }

  .top-bar h1 {
    font-size: 22px;
  }

  .count-badge {
    background: var(--orange);
    color: white;
    font-size: 12px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: var(--radius-full);
  }

  .search-wrapper {
    position: relative;
  }

  .search-box {
    position: relative;
    display: flex;
    align-items: center;
  }

  .search-icon {
    position: absolute;
    left: 14px;
    color: var(--gray-400);
    pointer-events: none;
  }

  .search-input {
    width: 100%;
    padding: var(--space-3) var(--space-4) var(--space-3) 42px;
    border: 1.5px solid var(--gray-200);
    border-radius: var(--radius-md);
    font-size: 15px;
    font-family: inherit;
    background: white;
    outline: none;
    transition: border-color var(--transition-fast);
    color: var(--dark);
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
    box-shadow: var(--shadow-sm);
    z-index: 10;
    overflow: hidden;
    border: 1px solid var(--gray-200);
    border-top: none;
  }

  .autocomplete-item {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    width: 100%;
    padding: var(--space-3) var(--space-4);
    border: none;
    background: none;
    cursor: pointer;
    font-family: inherit;
    font-size: 14px;
    text-align: left;
    transition: background var(--transition-fast);
  }

  .autocomplete-item:hover {
    background: var(--gray-50);
  }

  .ac-name {
    font-weight: 600;
    flex: 1;
  }

  .ac-size {
    color: var(--gray-500);
    font-size: 12px;
  }

  .list {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .advice-panel {
    position: sticky;
    bottom: 68px;
    background: white;
    border-radius: var(--radius-lg);
    padding: var(--space-4);
    box-shadow: var(--shadow-up);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .advice-header {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    font-size: 15px;
    color: var(--dark);
  }

  .mode-toggle {
    display: flex;
    gap: 0;
    background: var(--gray-100);
    border-radius: var(--radius-sm);
    padding: 3px;
  }

  .mode-btn {
    flex: 1;
    padding: 7px var(--space-3);
    border: none;
    border-radius: var(--radius-xs);
    background: transparent;
    font-size: 13px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all var(--transition-fast);
    color: var(--gray-600);
  }

  .mode-btn.active {
    background: white;
    color: var(--orange);
    box-shadow: var(--shadow-xs);
  }

  .advice-text {
    font-size: 14px;
    line-height: 1.5;
  }

  .advice-text strong {
    color: var(--orange);
  }
</style>
