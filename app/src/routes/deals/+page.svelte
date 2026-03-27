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

  <div class="store-tabs" role="tablist" aria-label="Filter op winkel">
    <button
      class="tab"
      class:active={activeFilter === 'alles'}
      role="tab"
      aria-selected={activeFilter === 'alles'}
      onclick={() => activeFilter = 'alles'}
    >Alles</button>
    {#each STORES as store}
      <button
        class="tab"
        class:active={activeFilter === store.id}
        role="tab"
        aria-selected={activeFilter === store.id}
        style:--tab-color={store.color}
        onclick={() => activeFilter = store.id}
      >
        {store.name}
      </button>
    {/each}
  </div>

  {#if activeFilter === 'alles'}
    <div class="toppers-section">
      <div class="toppers-bg">
        <div class="toppers-header">
          <h2 class="toppers-title">Oma's Toppers</h2>
        </div>
        <OmaBubble text="Dit zijn Oma's toppers deze week!" mood="excited" />
        <div class="toppers-list">
          {#each topDeals as deal}
            <DealCard {deal} />
          {/each}
        </div>
      </div>
    </div>
  {/if}

  <div class="section-header">
    <h2 class="section-title">Alle deals</h2>
    <span class="deal-count">{filteredDeals.length} deals</span>
  </div>
  <div class="deals-grid">
    {#each filteredDeals as deal}
      <DealCard {deal} />
    {/each}
  </div>
</div>

<style>
  .page {
    padding: var(--space-5);
    padding-bottom: 96px;
    display: flex;
    flex-direction: column;
    gap: var(--space-5);
    overflow-x: hidden;
  }

  .top-bar {
    padding: var(--space-1) 0;
  }

  .top-bar h1 {
    font-size: 24px;
  }

  .store-tabs {
    display: flex;
    gap: 8px;
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
    padding: 12px 18px;
    border-radius: var(--radius-full);
    border: 2px solid var(--gray-200);
    background: white;
    font-size: 14px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all var(--transition-fast);
    color: var(--gray-700);
    -webkit-tap-highlight-color: transparent;
  }

  .tab:active {
    transform: scale(0.95);
  }

  .tab.active {
    background: var(--tab-color, var(--orange));
    color: white;
    border-color: var(--tab-color, var(--orange));
    box-shadow: none;
  }

  .tab:hover:not(.active) {
    border-color: var(--gray-300);
    background: var(--gray-50);
  }

  .toppers-section {
    margin: 0 calc(-1 * var(--space-5));
  }

  .toppers-bg {
    background: linear-gradient(135deg, var(--orange-light) 0%, var(--orange-light) 50%, #FFF8F0 100%);
    padding: var(--space-5);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .toppers-header {
    display: flex;
    align-items: center;
    gap: var(--space-2);
  }

  .toppers-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--orange);
  }

  .toppers-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .section-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--dark);
  }

  .deal-count {
    font-size: 13px;
    font-weight: 600;
    color: var(--gray-500);
  }

  .deals-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-3);
  }
</style>
