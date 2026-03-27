<script lang="ts">
  import { DEALS } from '$lib/data/deals';
  import DealCard from '$lib/components/DealCard.svelte';
  import OmaBubble from '$lib/components/OmaBubble.svelte';
  import { toasts } from '$lib/stores/toast';

  const topDeals = DEALS.sort((a, b) => b.discount - a.discount).slice(0, 5);
</script>

<div class="page">
  <header class="top-bar">
    <h1 class="logo">Oma Zuinig</h1>
  </header>

  <div class="hero">
    <span class="hero-greeting">Hoi lieverd!</span>
    <p class="hero-text">Oma heeft vandaag</p>
    <span class="hero-amount">&euro;14,20</span>
    <p class="hero-text">voor je bespaard</p>
  </div>

  <OmaBubble text="Welkom terug! Ik heb mooie aanbiedingen voor je gevonden." />

  <div class="quick-actions">
    <a href="/lijst" class="action-btn">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <path d="M8 8h8M8 12h8M8 16h5"/>
      </svg>
      <span>Mijn Lijst</span>
    </a>
    <a href="/vergelijk" class="action-btn">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M8 3v18M16 3v18"/>
        <path d="M3 8h5M16 8h5"/>
        <path d="M3 16h5M16 16h5"/>
      </svg>
      <span>Vergelijk</span>
    </a>
    <button class="action-btn" onclick={() => toasts.show('Scanfunctie komt binnenkort!', 'info')}>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <path d="M7 7h0M7 12h0M7 17h0M12 7h0M12 12h0M12 17h0M17 7h0M17 12h0M17 17h0"/>
      </svg>
      <span>Scan</span>
    </button>
  </div>

  <h3 class="section-title">Vandaag in de aanbieding</h3>

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
    padding: var(--space-4);
    padding-bottom: 88px;
    display: flex;
    flex-direction: column;
    gap: var(--space-5);
    overflow-x: hidden;
  }

  .top-bar {
    padding: var(--space-1) 0;
  }

  .logo {
    color: var(--orange);
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  .hero {
    background: linear-gradient(135deg, #FF6200 0%, #FF8A3D 100%);
    color: white;
    border-radius: var(--radius-xl);
    padding: var(--space-8) var(--space-6);
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
  }

  .hero-greeting {
    font-size: 18px;
    font-weight: 500;
    opacity: 0.9;
    margin-bottom: var(--space-2);
  }

  .hero-text {
    font-size: 16px;
    font-weight: 400;
    opacity: 0.9;
    line-height: 1.3;
  }

  .hero-amount {
    font-size: 52px;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    margin: var(--space-2) 0;
  }

  .quick-actions {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: var(--space-3);
  }

  .action-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-2);
    background: white;
    border-radius: var(--radius-md);
    padding: var(--space-4) var(--space-2);
    text-decoration: none;
    color: var(--dark);
    border: none;
    cursor: pointer;
    font-family: inherit;
    font-size: 13px;
    font-weight: 600;
    transition: transform var(--transition-fast);
    box-shadow: var(--shadow-xs);
  }

  .action-btn:hover {
    transform: translateY(-1px);
  }

  .action-btn svg {
    color: var(--orange);
  }

  .section-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--dark);
  }

  .deals-carousel {
    display: flex;
    gap: var(--space-3);
    overflow-x: auto;
    padding-bottom: 4px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    margin: 0 calc(-1 * var(--space-4));
    padding-left: var(--space-4);
    padding-right: var(--space-4);
  }

  .deals-carousel::-webkit-scrollbar {
    display: none;
  }

  .deal-slide {
    flex-shrink: 0;
    width: 260px;
  }
</style>
