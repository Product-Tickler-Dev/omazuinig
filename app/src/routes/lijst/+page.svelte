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
    splitResult.storesUsed.map(id => getStore(id)?.name ?? id)
  );

  function addItem(productId: number) {
    shoppingList.add(productId);
    const product = getProduct(productId);
    toasts.show(`${product?.name ?? 'Product'} toegevoegd!`);
    searchQuery = '';
  }
</script>

<div class="page">
  <div class="page-meta">
    <span class="page-label">Boodschappenlijst</span>
    {#if items.length > 0}
      <span class="count-badge">{items.length}</span>
    {/if}
  </div>

  <div class="search-wrapper">
    <div class="search-box">
      <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
      <div class="autocomplete" role="listbox" aria-label="Zoekresultaten">
        {#each searchResults as product}
          <button class="autocomplete-item" role="option" aria-selected="false" onclick={() => addItem(product.id)}>
            <span class="ac-name">{product.name}</span>
            <span class="ac-price">{formatPrice(getCheapestStore(product)[1])}</span>
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
        <img src="/oma-avatar.png" alt="" class="advice-avatar" />
        <strong class="advice-title">Oma's Advies</strong>
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
      <div class="advice-content">
        {#if adviceMode === 'single'}
          <p class="advice-text">Ga naar <strong>{cheapestStoreName}</strong></p>
          <span class="advice-total">{formatPrice(cheapestStoreTotal)}</span>
        {:else}
          <div class="split-stores">
            {#each splitStoreNames as storeName}
              <span class="store-pill">{storeName}</span>
            {/each}
          </div>
          <span class="advice-total">{formatPrice(splitResult.splitTotal)}</span>
          <span class="advice-savings">Besparing: {formatPrice(splitResult.savings)}</span>
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
  .page {
    padding: var(--space-5);
    padding-bottom: 200px;
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
    overflow-x: hidden;
  }

  .page-meta {
    display: flex;
    align-items: center;
    gap: var(--space-2);
  }

  .page-label {
    font-size: 15px;
    font-weight: 600;
    color: var(--gray-600);
  }

  .count-badge {
    background: var(--orange);
    color: white;
    font-size: 13px;
    font-weight: 700;
    padding: 3px 12px;
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
    left: 16px;
    color: var(--gray-400);
    pointer-events: none;
  }

  .search-input {
    width: 100%;
    padding: 14px var(--space-4) 14px 48px;
    border: 2px solid var(--gray-200);
    border-radius: var(--radius-lg);
    font-size: 16px;
    font-family: inherit;
    background: white;
    outline: none;
    transition: all var(--transition-fast);
    color: var(--dark);
  }

  .search-input:focus {
    border-color: var(--orange);
    box-shadow: 0 0 0 3px rgba(255, 98, 0, 0.08);
  }

  .autocomplete {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    right: 0;
    background: white;
    border-radius: var(--radius-md);
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border: 1px solid #F0F0F0;
    z-index: 10;
    overflow: hidden;
    animation: fadeIn 0.15s ease;
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
    font-size: 15px;
    text-align: left;
    transition: background var(--transition-fast);
    border-bottom: 1px solid var(--gray-100);
  }

  .autocomplete-item:last-child {
    border-bottom: none;
  }

  .autocomplete-item:hover {
    background: var(--gray-50);
  }

  .ac-name {
    font-weight: 600;
    flex: 1;
  }

  .ac-price {
    font-weight: 700;
    font-size: 13px;
    color: var(--green-dark);
    background: var(--green-light);
    padding: 2px 8px;
    border-radius: var(--radius-full);
  }

  .ac-size {
    color: var(--gray-500);
    font-size: 12px;
  }

  .list {
    display: flex;
    flex-direction: column;
  }

  .advice-panel {
    position: sticky;
    bottom: 72px;
    background: white;
    padding: var(--space-5);
    border-top: 1px solid #E8E8E8;
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .advice-header {
    display: flex;
    align-items: center;
    gap: var(--space-3);
  }

  .advice-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 2px 6px rgba(255, 98, 0, 0.15);
  }

  .advice-title {
    font-size: 16px;
    color: var(--dark);
  }

  .mode-toggle {
    display: flex;
    gap: 0;
    background: var(--gray-100);
    border-radius: var(--radius-full);
    padding: 3px;
  }

  .mode-btn {
    flex: 1;
    padding: 8px var(--space-3);
    border: none;
    border-radius: var(--radius-full);
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
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }

  .advice-content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-2);
  }

  .advice-text {
    font-size: 14px;
    line-height: 1.5;
  }

  .advice-text strong {
    color: var(--orange);
  }

  .advice-total {
    font-size: 32px;
    font-weight: 700;
    color: var(--green-dark);
    letter-spacing: -0.02em;
    line-height: 1;
  }

  .advice-savings {
    font-size: 14px;
    font-weight: 600;
    color: var(--green-dark);
    background: var(--green-light);
    padding: 4px 12px;
    border-radius: var(--radius-full);
  }

  .split-stores {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-1);
  }

  .store-pill {
    font-size: 12px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: var(--radius-full);
    background: var(--orange-light);
    color: var(--orange);
  }
</style>
