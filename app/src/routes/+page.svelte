<script lang="ts">
  import { DEALS } from '$lib/data/deals';
  import DealCard from '$lib/components/DealCard.svelte';
  import OmaBubble from '$lib/components/OmaBubble.svelte';
  import { toasts } from '$lib/stores/toast';

  const topDeals = DEALS.sort((a, b) => b.discount - a.discount).slice(0, 5);
</script>

<div class="page">
  <header class="top-bar">
    <img src="/oma-avatar.png" alt="Oma" class="top-avatar" />
    <h1 class="logo">Oma Zuinig</h1>
  </header>

  <div class="hero">
    <div class="hero-content">
      <span class="hero-greeting">Hoi lieverd!</span>
      <p class="hero-text">Oma heeft vandaag</p>
      <span class="hero-amount">&euro;14,20</span>
      <p class="hero-text">voor je bespaard</p>
    </div>
    <div class="hero-image">
      <img src="/oma-hero.png" alt="Oma Zuinig helpt je besparen" class="hero-img" />
    </div>
  </div>

  <div class="bubble-section">
    <OmaBubble text="Welkom terug! Ik heb mooie aanbiedingen voor je gevonden." />
  </div>

  <div class="quick-actions">
    <a href="/lijst" class="action-btn action-orange">
      <div class="action-icon-wrap">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2"/>
          <path d="M8 8h8M8 12h8M8 16h5"/>
        </svg>
      </div>
      <span class="action-label">Mijn Lijst</span>
    </a>
    <a href="/vergelijk" class="action-btn action-green">
      <div class="action-icon-wrap">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 3v18M16 3v18"/>
          <path d="M3 8h5M16 8h5"/>
          <path d="M3 16h5M16 16h5"/>
        </svg>
      </div>
      <span class="action-label">Vergelijk</span>
    </a>
    <button class="action-btn action-blue" onclick={() => toasts.show('Scanfunctie komt binnenkort!', 'info')}>
      <div class="action-icon-wrap">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2"/>
          <path d="M7 7h0M7 12h0M7 17h0M12 7h0M12 12h0M12 17h0M17 7h0M17 12h0M17 17h0"/>
        </svg>
      </div>
      <span class="action-label">Scan</span>
    </button>
  </div>

  <div class="section-header">
    <h3 class="section-title">Aanbiedingen</h3>
    <a href="/deals" class="section-link">Bekijk alles</a>
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
    padding: var(--space-5);
    padding-bottom: 96px;
    display: flex;
    flex-direction: column;
    gap: var(--space-6);
    overflow-x: hidden;
  }

  .top-bar {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-1) 0;
  }

  .top-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 2px 8px rgba(255, 98, 0, 0.2);
  }

  .logo {
    color: var(--orange);
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  .hero {
    background: linear-gradient(135deg, #FF6200 0%, #FF8A3D 60%, #FFB06B 100%);
    color: white;
    border-radius: var(--radius-xl);
    padding: var(--space-6);
    display: flex;
    align-items: center;
    gap: var(--space-4);
    box-shadow: var(--shadow-orange);
    position: relative;
    overflow: hidden;
    min-height: 180px;
  }

  .hero::before {
    content: '';
    position: absolute;
    top: -30%;
    right: -10%;
    width: 200px;
    height: 200px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 50%;
  }

  .hero::after {
    content: '';
    position: absolute;
    bottom: -20%;
    left: 10%;
    width: 120px;
    height: 120px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 50%;
  }

  .hero-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
    z-index: 1;
  }

  .hero-greeting {
    font-size: 18px;
    font-weight: 500;
    opacity: 0.9;
    margin-bottom: var(--space-1);
  }

  .hero-text {
    font-size: 15px;
    font-weight: 400;
    opacity: 0.85;
    line-height: 1.3;
  }

  .hero-amount {
    font-size: 56px;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1;
    text-shadow: 0 3px 12px rgba(0, 0, 0, 0.15);
    margin: var(--space-1) 0;
  }

  .hero-image {
    flex-shrink: 0;
    z-index: 1;
  }

  .hero-img {
    width: 120px;
    height: 120px;
    object-fit: contain;
    filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.15));
  }

  .bubble-section {
    margin-top: -8px;
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
    border-radius: var(--radius-lg);
    padding: var(--space-5) var(--space-2);
    text-decoration: none;
    color: var(--dark);
    border: none;
    cursor: pointer;
    font-family: inherit;
    transition: all var(--transition-fast);
    -webkit-tap-highlight-color: transparent;
  }

  .action-btn:active {
    transform: scale(0.96);
  }

  .action-btn:hover {
    transform: translateY(-2px);
  }

  .action-orange {
    background: var(--orange-light);
  }

  .action-orange .action-icon-wrap {
    color: var(--orange);
  }

  .action-green {
    background: var(--green-light);
  }

  .action-green .action-icon-wrap {
    color: var(--green-dark);
  }

  .action-blue {
    background: var(--blue-light);
  }

  .action-blue .action-icon-wrap {
    color: var(--blue);
  }

  .action-icon-wrap {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-xs);
  }

  .action-label {
    font-size: 13px;
    font-weight: 700;
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

  .section-link {
    font-size: 14px;
    font-weight: 600;
    color: var(--orange);
    text-decoration: none;
  }

  .section-link:hover {
    text-decoration: underline;
  }

  .deals-carousel {
    display: flex;
    gap: var(--space-3);
    overflow-x: auto;
    padding-bottom: 4px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    margin: 0 calc(-1 * var(--space-5));
    padding-left: var(--space-5);
    padding-right: var(--space-5);
  }

  .deals-carousel::-webkit-scrollbar {
    display: none;
  }

  .deal-slide {
    flex-shrink: 0;
    width: 240px;
  }
</style>
