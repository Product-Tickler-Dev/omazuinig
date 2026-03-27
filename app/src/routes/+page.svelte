<script lang="ts">
  import { DEALS } from '$lib/data/deals';
  import DealCard from '$lib/components/DealCard.svelte';
  import OmaBubble from '$lib/components/OmaBubble.svelte';
  import { toasts } from '$lib/stores/toast';

  const topDeals = DEALS.sort((a, b) => b.discount - a.discount).slice(0, 5);
</script>

<div class="page">
  <header class="top-bar">
    <h1 class="logo">&#x1F475; Oma Zuinig</h1>
  </header>

  <div class="hero">
    <h2>Hoi lieverd!</h2>
    <p>Oma heeft vandaag <span class="amount">&euro;14,20</span> voor je bespaard!</p>
  </div>

  <div class="quick-actions">
    <a href="/lijst" class="action-card">
      <span class="action-icon">&#x1F6D2;</span>
      <span class="action-label">Mijn Lijst</span>
    </a>
    <a href="/vergelijk" class="action-card">
      <span class="action-icon">&#x1F50D;</span>
      <span class="action-label">Vergelijk</span>
    </a>
    <button class="action-card" onclick={() => toasts.show('Scanfunctie komt binnenkort!', 'info')}>
      <span class="action-icon">&#x1F4F7;</span>
      <span class="action-label">Scan</span>
    </button>
  </div>

  <div class="section-header">
    <h3>Vandaag in de aanbieding</h3>
    <OmaBubble text="Dit wil je niet missen!" />
  </div>

  <div class="deals-carousel">
    {#each topDeals as deal}
      <div class="deal-slide">
        <DealCard {deal} />
      </div>
    {/each}
  </div>
</div>

<style>
  .page {
    padding: 16px;
    padding-bottom: 80px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .top-bar {
    padding: 4px 0;
  }

  .logo {
    color: var(--orange);
    font-size: 24px;
    font-weight: 700;
  }

  .hero {
    background: linear-gradient(135deg, #FF6200, #FF8A3D);
    color: white;
    border-radius: 20px;
    padding: 24px;
  }

  .hero h2 {
    font-size: 22px;
    margin-bottom: 8px;
  }

  .hero p {
    font-size: 16px;
    line-height: 1.4;
  }

  .amount {
    font-size: 28px;
    font-weight: 700;
    display: inline-block;
  }

  .quick-actions {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12px;
  }

  .action-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    background: white;
    border-radius: var(--radius-md);
    padding: 16px 8px;
    box-shadow: var(--shadow-sm);
    text-decoration: none;
    color: var(--dark);
    border: none;
    cursor: pointer;
    font-family: inherit;
    transition: transform 0.15s;
  }

  .action-card:hover {
    transform: translateY(-2px);
  }

  .action-icon {
    font-size: 28px;
  }

  .action-label {
    font-size: 13px;
    font-weight: 700;
  }

  .section-header {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .deals-carousel {
    display: flex;
    gap: 12px;
    overflow-x: auto;
    padding-bottom: 4px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .deals-carousel::-webkit-scrollbar {
    display: none;
  }

  .deal-slide {
    flex-shrink: 0;
    width: 280px;
  }
</style>
