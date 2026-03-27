<script lang="ts">
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
</script>

<div class="page">
  <header class="top-bar">
    <h1>Mijn Oma</h1>
  </header>

  <div class="profile-hero">
    <div class="avatar-glow">
      <img src="/oma-avatar.png" alt="Oma Zuinig" class="profile-avatar" />
    </div>
    <span class="savings-amount">&euro;847,30</span>
    <span class="savings-label">totaal bespaard</span>
  </div>

  <OmaBubble text="Goed bezig, lieverd! Je bespaart steeds meer." />

  <div class="stats-row">
    <div class="stat">
      <span class="stat-value">&euro;14,20</span>
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

  <div class="chart-section">
    <h3>Besparingen per week</h3>
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
      <h3>Koopjeskoning</h3>
      <span class="level-pct">62%</span>
    </div>
    <div class="progress-track">
      <div class="progress-fill" style:width="62%"></div>
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
  </div>

  <div class="settings-section">
    <h3>Instellingen</h3>
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

  .top-bar {
    padding: var(--space-1) 0;
  }

  .top-bar h1 {
    font-size: 24px;
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
    box-shadow: 0 8px 32px rgba(255, 98, 0, 0.25), 0 0 0 8px rgba(255, 98, 0, 0.06);
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
    background: white;
    border-radius: var(--radius-lg);
    padding: var(--space-5);
    box-shadow: var(--shadow-sm);
  }

  .chart-section h3 {
    margin-bottom: var(--space-5);
    font-size: 17px;
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
    background: white;
    border-radius: var(--radius-lg);
    padding: var(--space-5);
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .level-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .level-header h3 {
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
    background: linear-gradient(90deg, #FF6200, #FF8A3D, #FFB06B);
    border-radius: var(--radius-full);
    transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 2px 8px rgba(255, 98, 0, 0.3);
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

  .settings-section {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .settings-section h3 {
    font-size: 17px;
    margin-bottom: var(--space-2);
  }

  .setting-row {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    background: white;
    padding: var(--space-4);
    border-radius: var(--radius-sm);
    box-shadow: var(--shadow-xs);
    border: none;
    cursor: pointer;
    font-family: inherit;
    width: 100%;
    text-align: left;
    transition: all var(--transition-fast);
  }

  .setting-row:hover {
    background: var(--gray-50);
    transform: translateX(2px);
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
</style>
