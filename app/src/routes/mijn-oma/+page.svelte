<script lang="ts">
  import { onMount } from 'svelte';
  import OmaBubble from '$lib/components/OmaBubble.svelte';

  const weeklyData = [
    { label: 'W9', amount: 9.80 },
    { label: 'W10', amount: 15.40 },
    { label: 'W11', amount: 8.20 },
    { label: 'W12', amount: 12.60 },
    { label: 'W13', amount: 11.90 },
    { label: 'W14', amount: 14.20 }
  ];

  const maxAmount = Math.max(...weeklyData.map(w => w.amount));
  const weeklyAvg = weeklyData.reduce((sum, w) => sum + w.amount, 0) / weeklyData.length;
  const thisWeek = 14.20;
  const aboveAverage = thisWeek > weeklyAvg;

  const levelSteps = [
    { name: 'Beginner', pct: 0 },
    { name: 'Spaarder', pct: 33 },
    { name: 'Koopjeskoning', pct: 66 },
    { name: 'Expert', pct: 100 }
  ];

  const settings = [
    { label: 'Postcode', value: '1234 AB' },
    { label: 'Favoriete winkel', value: 'Albert Heijn' },
    { label: 'Meldingen', value: 'Aan' },
    { label: 'Huishouden', value: '2 personen' }
  ];

  let displayAmount = $state(0);
  let shimmerDone = $state(false);

  onMount(() => {
    const target = 847.30;
    const duration = 1500;
    const start = performance.now();

    function easeOut(t: number): number {
      return 1 - Math.pow(1 - t, 3);
    }

    function tick(now: number) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      displayAmount = target * easeOut(progress);
      if (progress < 1) {
        requestAnimationFrame(tick);
      } else {
        displayAmount = target;
      }
    }

    requestAnimationFrame(tick);

    // Trigger shimmer after bar animates
    setTimeout(() => { shimmerDone = true; }, 1200);
  });

  let formattedAmount = $derived(
    '\u20AC' + displayAmount.toFixed(2).replace('.', ',')
  );
</script>

<div class="page">
  <div class="profile-hero">
    <div class="avatar-glow">
      <img src="/oma-avatar.png" alt="Oma Zuinig" class="profile-avatar" />
    </div>
    <span class="savings-amount">{formattedAmount}</span>
    <span class="savings-label">totaal bespaard</span>
  </div>

  <div class="oma-bubble-wrap">
    <OmaBubble text="Goed bezig, lieverd! Je bespaart steeds meer." mood="proud" />
  </div>

  <div class="stats-row">
    <div class="stat stat-highlight">
      <span class="stat-value stat-value-week">&euro;14,20 {#if aboveAverage}<span class="arrow-up">&#9650;</span>{/if}</span>
      <span class="stat-label">Deze week</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat">
      <span class="stat-value">&euro;63,40</span>
      <span class="stat-label">Deze maand</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat">
      <span class="stat-value">&euro;11,20</span>
      <span class="stat-label">Gem./week</span>
    </div>
  </div>

  <div class="data-row">
    <div class="chart-section">
      <h2 class="section-heading">Besparingen per week</h2>
      <div class="chart">
        {#each weeklyData as week, i}
          <div class="bar-wrapper">
            <div
              class="bar"
              style:height="{(week.amount / maxAmount) * 100}%"
              style:animation-delay="{i * 80}ms"
            >
              <span class="bar-value">&euro;{week.amount.toFixed(0)}</span>
            </div>
            <span class="bar-label">{week.label}</span>
          </div>
        {/each}
      </div>
    </div>

    <div class="level-section">
    <div class="level-header">
      <h2 class="section-heading">Koopjeskoning</h2>
      <span class="level-pct">62%</span>
    </div>
    <div class="progress-track">
      <div class="progress-fill" class:shimmer={shimmerDone} style:--progress="0.62"></div>
      <div class="oma-on-bar" style:left="62%">
        <img src="/oma-avatar.png" alt="" class="bar-oma" />
      </div>
      <div class="level-dots">
        {#each levelSteps as step}
          <div class="level-dot" style:left="{step.pct}%" class:reached={62 >= step.pct}>
            <span class="dot-marker"></span>
          </div>
        {/each}
      </div>
    </div>
    <div class="level-labels">
      {#each levelSteps as step}
        <span class="level-name" class:current={step.name === 'Koopjeskoning'}>{step.name}</span>
      {/each}
    </div>
    <p class="level-motivation">Nog &euro;153 tot Expert!</p>
  </div>
  </div>

  <div class="settings-section">
    <h2 class="section-heading">Instellingen</h2>
    {#each settings as setting}
      <button class="setting-row">
        <span class="setting-label">{setting.label}</span>
        <span class="setting-value">{setting.value}</span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 18l6-6-6-6"/>
        </svg>
      </button>
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

  .profile-hero {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-4) 0;
  }

  .avatar-glow {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    padding: 3px;
    background: linear-gradient(135deg, var(--orange) 0%, var(--orange-warm, #FF8A3D) 100%);
    box-shadow: var(--shadow-orange), 0 0 0 8px rgba(255, 98, 0, 0.06);
    margin-bottom: var(--space-2);
  }

  .profile-avatar {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    display: block;
  }

  .savings-amount {
    font-size: 56px;
    font-weight: 700;
    color: var(--green-dark);
    letter-spacing: -0.03em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
  }

  .savings-label {
    font-size: 15px;
    color: var(--gray-500);
    font-weight: 500;
  }

  .stats-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-5);
    padding: var(--space-4) 0;
  }

  .stat {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
  }

  .stat-value {
    font-size: 20px;
    font-weight: 700;
    color: var(--dark);
    letter-spacing: -0.01em;
  }

  .stat-value-week {
    font-size: 28px;
    font-weight: 700;
    color: var(--green-dark);
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .arrow-up {
    font-size: 14px;
    color: var(--green);
    line-height: 1;
  }

  .stat-label {
    font-size: 12px;
    color: var(--gray-500);
    font-weight: 500;
  }

  .stat-divider {
    width: 1px;
    height: 36px;
    background: var(--gray-200);
  }

  .chart-section {
    background: #F8F8F8;
    border-radius: var(--radius-lg);
    padding: var(--space-5);
  }

  .section-heading {
    font-size: 17px;
  }

  .chart-section .section-heading {
    margin-bottom: var(--space-5);
  }

  .chart {
    display: flex;
    align-items: flex-end;
    gap: var(--space-3);
    height: 130px;
  }

  .bar-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    justify-content: flex-end;
    gap: var(--space-2);
  }

  .bar {
    width: 12px;
    background: linear-gradient(180deg, var(--green) 0%, #00A044 100%);
    border-radius: 6px 6px 3px 3px;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    min-height: 20px;
    animation: barGrow 0.6s ease-out both;
  }

  @keyframes barGrow {
    from {
      transform: scaleY(0);
      transform-origin: bottom;
    }
    to {
      transform: scaleY(1);
      transform-origin: bottom;
    }
  }

  .bar-value {
    font-size: 10px;
    font-weight: 700;
    color: white;
    padding-top: 4px;
    white-space: nowrap;
  }

  .bar-label {
    font-size: 11px;
    color: var(--gray-500);
    font-weight: 600;
  }

  .level-section {
    background: #F8F8F8;
    border-radius: var(--radius-lg);
    padding: var(--space-5);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .level-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .level-header .section-heading {
    font-size: 17px;
  }

  .level-pct {
    font-size: 15px;
    font-weight: 700;
    color: var(--orange);
  }

  .progress-track {
    position: relative;
    height: 12px;
    background: var(--gray-100);
    border-radius: var(--radius-full);
    overflow: visible;
  }

  .progress-fill {
    height: 100%;
    width: 100%;
    background: linear-gradient(90deg, var(--orange), var(--orange-warm), #FFB06B);
    border-radius: var(--radius-full);
    transform: scaleX(var(--progress));
    transform-origin: left;
    transition: transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 2px 8px rgba(255, 98, 0, 0.3);
    position: relative;
    overflow: hidden;
  }

  .progress-fill.shimmer::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.4) 50%, transparent 100%);
    animation: shimmerSweep 1s ease-out forwards;
  }

  @keyframes shimmerSweep {
    from { left: -100%; }
    to { left: 200%; }
  }

  .oma-on-bar {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: 3;
    animation: fadeIn 0.5s ease-out 0.8s both;
  }

  .bar-oma {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid white;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
    display: block;
  }

  .level-dots {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 100%;
  }

  .level-dot {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
  }

  .dot-marker {
    display: block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--gray-300);
    border: 2px solid white;
    transition: all var(--transition-base);
  }

  .level-dot.reached .dot-marker {
    background: var(--orange);
    box-shadow: 0 1px 4px rgba(255, 98, 0, 0.3);
  }

  .level-labels {
    display: flex;
    justify-content: space-between;
    padding: 0 0;
  }

  .level-name {
    font-size: 10px;
    color: var(--gray-400);
    font-weight: 500;
  }

  .level-name.current {
    color: var(--orange);
    font-weight: 700;
  }

  .level-motivation {
    font-size: 13px;
    font-weight: 600;
    color: var(--orange);
    text-align: center;
  }

  .settings-section {
    display: flex;
    flex-direction: column;
  }

  .settings-section .section-heading {
    font-size: 17px;
    margin-bottom: var(--space-2);
  }

  .setting-row {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    background: transparent;
    padding: var(--space-4) 0;
    border: none;
    border-bottom: 1px solid #F0F0F0;
    cursor: pointer;
    font-family: inherit;
    width: 100%;
    text-align: left;
    transition: background var(--transition-fast);
  }

  .setting-row:hover {
    background: var(--gray-50);
  }

  .setting-label {
    flex: 1;
    font-weight: 600;
    font-size: 15px;
    color: var(--dark);
  }

  .setting-value {
    font-size: 14px;
    color: var(--gray-500);
  }

  .setting-row svg {
    color: var(--gray-300);
    flex-shrink: 0;
  }

  .data-row {
    display: contents;
  }

  @media (min-width: 768px) {
    .page {
      max-width: 900px;
      margin: 0 auto;
      padding-bottom: var(--space-4);
      gap: var(--space-3);
    }

    .profile-hero {
      padding: var(--space-2) 0;
      gap: var(--space-1);
    }

    .avatar-glow {
      width: 56px;
      height: 56px;
    }

    .savings-amount {
      font-size: 40px;
    }

    .oma-bubble-wrap {
      display: none;
    }

    .stats-row {
      gap: var(--space-8);
      padding: var(--space-2) 0;
    }

    .data-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: var(--space-3);
    }

    .chart-section {
      padding: var(--space-4);
    }

    .chart {
      height: 120px;
    }

    .level-section {
      padding: var(--space-4);
    }

    .settings-section {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0 var(--space-6);
    }

    .settings-section .section-heading {
      grid-column: 1 / -1;
    }

    .setting-row {
      padding: var(--space-3) 0;
    }
  }
</style>
