<script lang="ts">
  import '../app.css';
  import BottomNav from '$lib/components/BottomNav.svelte';
  import Toast from '$lib/components/Toast.svelte';
  import Celebration from '$lib/components/Celebration.svelte';

  let { children } = $props();
</script>

<div class="app-shell">
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
</style>
