<script lang="ts">
  import '../app.css';
  import BottomNav from '$lib/components/BottomNav.svelte';
  import Toast from '$lib/components/Toast.svelte';
  import Celebration from '$lib/components/Celebration.svelte';

  let { children } = $props();
</script>

<div class="app-shell">
  <header class="app-header">
    <img src="/oma-avatar.png" alt="" class="header-oma" />
    <span class="header-title">Oma Zuinig</span>
  </header>
  {@render children()}
  <BottomNav />
  <Toast />
  <Celebration />
</div>

<style>
  .app-shell {
    max-width: 480px;
    margin: 0 auto;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
    background: linear-gradient(180deg, white 0%, #FFF9F5 40%, #FFFAF7 100%);
  }

  .app-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px 4px;
  }

  .header-oma {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    object-fit: cover;
  }

  .header-title {
    font-size: 26px;
    font-weight: 700;
    color: var(--orange);
    letter-spacing: -0.02em;
  }
</style>
