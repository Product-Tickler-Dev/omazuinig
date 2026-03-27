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
    { icon: '\u{1F4CD}', label: 'Postcode', value: '1234 AB' },
    { icon: '\u{1F3EA}', label: 'Favoriete winkel', value: 'Albert Heijn' },
    { icon: '\u{1F514}', label: 'Meldingen', value: 'Aan' },
    { icon: '\u{1F46A}', label: 'Huishouden', value: '2 personen' }
  ];
</script>

<div class="page">
  <header class="top-bar">
    <h1>&#x1F475; Mijn Oma</h1>
  </header>

  <div class="oma-hero">
    <span class="oma-big">&#x1F475;</span>
    <OmaBubble text="Goed bezig, lieverd!" />
  </div>

  <div class="savings-counter">
    <span class="savings-amount">&euro;847,30</span>
    <span class="savings-label">totaal bespaard</span>
  </div>

  <div class="stats-row">
    <div class="stat-card">
      <span class="stat-value">&euro;14,20</span>
      <span class="stat-label">Deze week</span>
    </div>
    <div class="stat-card">
      <span class="stat-value">&euro;63,40</span>
      <span class="stat-label">Deze maand</span>
    </div>
    <div class="stat-card">
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
    <h3>&#x1F451; Koopjeskoning</h3>
    <div class="progress-bar">
      <div class="progress-fill" style:width="62%"></div>
    </div>
    <div class="level-labels">
      <span>Beginner</span>
      <span class="level-current">62%</span>
      <span>Expert</span>
    </div>
  </div>

  <div class="settings-section">
    <h3>Instellingen</h3>
    {#each settings as setting}
      <div class="setting-row">
        <span class="setting-icon">{setting.icon}</span>
        <span class="setting-label">{setting.label}</span>
        <span class="setting-value">{setting.value}</span>
        <span class="setting-arrow">&#x203A;</span>
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

  .top-bar h1 {
    font-size: 22px;
  }

  .oma-hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }

  .oma-big {
    font-size: 80px;
    line-height: 1;
  }

  .savings-counter {
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .savings-amount {
    font-size: 42px;
    font-weight: 700;
    color: var(--green);
  }

  .savings-label {
    font-size: 14px;
    color: #888;
  }

  .stats-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
  }

  .stat-card {
    background: white;
    border-radius: var(--radius-md);
    padding: 14px 10px;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }

  .stat-value {
    font-size: 18px;
    font-weight: 700;
    color: var(--dark);
  }

  .stat-label {
    font-size: 12px;
    color: #888;
  }

  .chart-section {
    background: white;
    border-radius: var(--radius-md);
    padding: 16px;
    box-shadow: var(--shadow-sm);
  }

  .chart-section h3 {
    margin-bottom: 12px;
    font-size: 16px;
  }

  .chart {
    display: flex;
    align-items: flex-end;
    gap: 8px;
    height: 120px;
  }

  .bar-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    justify-content: flex-end;
    gap: 4px;
  }

  .bar {
    width: 100%;
    background: var(--green);
    border-radius: 6px 6px 0 0;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    min-height: 16px;
    transition: height 0.4s ease;
  }

  .bar-value {
    font-size: 10px;
    font-weight: 700;
    color: white;
    padding-top: 4px;
  }

  .bar-label {
    font-size: 11px;
    color: #888;
    font-weight: 600;
  }

  .level-section {
    background: white;
    border-radius: var(--radius-md);
    padding: 16px;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .level-section h3 {
    font-size: 16px;
  }

  .progress-bar {
    height: 12px;
    background: #eee;
    border-radius: 999px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #FF6200, #FF8A3D);
    border-radius: 999px;
    transition: width 0.5s ease;
  }

  .level-labels {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #888;
  }

  .level-current {
    font-weight: 700;
    color: var(--orange);
  }

  .settings-section {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .settings-section h3 {
    font-size: 16px;
    margin-bottom: 8px;
  }

  .setting-row {
    display: flex;
    align-items: center;
    gap: 12px;
    background: white;
    padding: 14px 16px;
    border-radius: var(--radius-sm);
    box-shadow: var(--shadow-sm);
  }

  .setting-icon {
    font-size: 20px;
    flex-shrink: 0;
  }

  .setting-label {
    flex: 1;
    font-weight: 600;
    font-size: 14px;
  }

  .setting-value {
    font-size: 13px;
    color: #888;
  }

  .setting-arrow {
    font-size: 20px;
    color: #ccc;
  }
</style>
