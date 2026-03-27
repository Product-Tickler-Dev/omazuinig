<script lang="ts">
  import { DEALS } from '$lib/data/deals';
  import { STORES } from '$lib/data/stores';
  import DealCard from '$lib/components/DealCard.svelte';
  import OmaBubble from '$lib/components/OmaBubble.svelte';

  let activeFilter = $state('alles');

  let sortedDeals = $derived(
    [...DEALS].sort((a, b) => b.discount - a.discount)
  );

  let topDeals = $derived(sortedDeals.slice(0, 3));

  let filteredDeals = $derived(
    activeFilter === 'alles'
      ? sortedDeals
      : sortedDeals.filter(d => d.store === activeFilter)
  );
</script>

<div class="page">
  <header class="top-bar">
    <h1>Aanbiedingen</h1>
  </header>

  <div class="store-tabs">
    <button
      class="tab"
      class:active={activeFilter === 'alles'}
      onclick={() => activeFilter = 'alles'}
    >Alles</button>
    {#each STORES as store}
      <button
        class="tab"
        class:active={activeFilter === store.id}
        style:--tab-color={store.color}
        onclick={() => activeFilter = store.id}
      >
        {store.name}
      </button>
    {/each}
  </div>

  {#if activeFilter === 'alles'}
    <div class="toppers-section">
      <h3 class="section-title">Oma's Toppers</h3>
      <OmaBubble text="Dit zijn Oma's toppers deze week!" />
      <div class="toppers-list">
        {#each topDeals as deal}
          <DealCard {deal} />
        {/each}
      </div>
    </div>
  {/if}

  <h3 class="section-title">Alle deals</h3>
  <div class="deals-grid">
    {#each filteredDeals as deal}
      <DealCard {deal} />
    {/each}
  </div>
</div>

<style>
  .page {
    padding: var(--space-4);
    padding-bottom: 88px;
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
    overflow-x: hidden;
  }

  .top-bar {
    padding: var(--space-1) 0;
  }

  .top-bar h1 {
    font-size: 22px;
  }

  .store-tabs {
    display: flex;
    gap: 6px;
    overflow-x: auto;
    padding: 2px 0;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .store-tabs::-webkit-scrollbar {
    display: none;
  }

  .tab {
    flex-shrink: 0;
    padding: 7px 16px;
    border-radius: var(--radius-full);
    border: 1.5px solid var(--gray-200);
    background: white;
    font-size: 13px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all var(--transition-fast);
    color: var(--gray-700);
  }

  .tab.active {
    background: var(--tab-color, var(--orange));
    color: white;
    border-color: var(--tab-color, var(--orange));
  }

  .tab:hover:not(.active) {
    border-color: var(--gray-300);
    background: var(--gray-50);
  }

  .section-title {
    font-size: 17px;
    font-weight: 700;
    color: var(--dark);
  }

  .toppers-section {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .toppers-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
  }

  .deals-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-3);
  }
</style>
