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
    <h1>&#x1F3F7;&#xFE0F; Aanbiedingen</h1>
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
      <div class="toppers-header">
        <h3>Oma's Toppers</h3>
      </div>
      <OmaBubble text="Dit zijn Oma's toppers!" />
      <div class="toppers-list">
        {#each topDeals as deal}
          <DealCard {deal} />
        {/each}
      </div>
    </div>
  {/if}

  <div class="deals-grid">
    {#each filteredDeals as deal}
      <DealCard {deal} />
    {/each}
  </div>
</div>

<style>
  .page {
    padding: 16px;
    padding-bottom: 80px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .top-bar {
    padding: 4px 0;
  }

  .top-bar h1 {
    font-size: 22px;
  }

  .store-tabs {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 4px 0;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .store-tabs::-webkit-scrollbar {
    display: none;
  }

  .tab {
    flex-shrink: 0;
    padding: 8px 16px;
    border-radius: 999px;
    border: 2px solid #e0e0e0;
    background: white;
    font-size: 13px;
    font-weight: 700;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s;
    color: var(--dark);
  }

  .tab.active {
    background: var(--tab-color, var(--orange));
    color: white;
    border-color: var(--tab-color, var(--orange));
  }

  .toppers-section {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .toppers-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .deals-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
</style>
