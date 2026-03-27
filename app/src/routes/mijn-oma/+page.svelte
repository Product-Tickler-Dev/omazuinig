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

  <div class="savings-hero">
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
      {#each weeklyData as week}
        <div class="bar-wrapper">
          <div class="bar" style:height="{(week.amount / maxAmount) * 100}%">
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
    <div class="progress-bar">
      <div class="progress-fill" style:width="62%"></div>
    </div>
    <div class="level-labels">
      <span>Beginner</span>
      <span>Expert</span>
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

  .top-bar h1 {
    font-size: 22px;
  }

  .savings-hero {
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
    padding: var(--space-6) 0 var(--space-2);
  }

  .savings-amount {
    font-size: 56px;
    font-weight: 700;
    color: var(--green-dark);
    letter-spacing: -0.03em;
    line-height: 1;
  }

  .savings-label {
    font-size: 14px;
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
    gap: 2px;
  }

  .stat-value {
    font-size: 18px;
    font-weight: 700;
    color: var(--dark);
  }

  .stat-label {
    font-size: 12px;
    color: var(--gray-500);
    font-weight: 500;
  }

  .stat-divider {
    width: 1px;
    height: 32px;
    background: var(--gray-200);
  }

  .chart-section {
    background: white;
    border-radius: var(--radius-md);
    padding: var(--space-4);
    box-shadow: var(--shadow-xs);
  }

  .chart-section h3 {
    margin-bottom: var(--space-4);
    font-size: 16px;
  }

  .chart {
    display: flex;
    align-items: flex-end;
    gap: var(--space-2);
    height: 120px;
  }

  .bar-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    justify-content: flex-end;
    gap: var(--space-1);
  }

  .bar {
    width: 100%;
    max-width: 32px;
    background: linear-gradient(180deg, var(--green) 0%, #00A044 100%);
    border-radius: 4px 4px 0 0;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    min-height: 16px;
    transition: height 0.4s ease;
  }

  .bar-value {
    font-size: 9px;
    font-weight: 700;
    color: white;
    padding-top: 4px;
  }

  .bar-label {
    font-size: 11px;
    color: var(--gray-500);
    font-weight: 500;
  }

  .level-section {
    background: white;
    border-radius: var(--radius-md);
    padding: var(--space-4);
    box-shadow: var(--shadow-xs);
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
    font-size: 16px;
  }

  .level-pct {
    font-size: 14px;
    font-weight: 700;
    color: var(--orange);
  }

  .progress-bar {
    height: 8px;
    background: var(--gray-100);
    border-radius: var(--radius-full);
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #FF6200, #FF8A3D);
    border-radius: var(--radius-full);
    transition: width 0.5s ease;
  }

  .level-labels {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: var(--gray-400);
    font-weight: 500;
  }

  .settings-section {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .settings-section h3 {
    font-size: 16px;
    margin-bottom: var(--space-2);
  }

  .setting-row {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    background: white;
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-sm);
    box-shadow: var(--shadow-xs);
    border: none;
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
    font-size: 14px;
    color: var(--dark);
  }

  .setting-value {
    font-size: 13px;
    color: var(--gray-500);
  }

  .setting-row svg {
    color: var(--gray-300);
    flex-shrink: 0;
  }
</style>
