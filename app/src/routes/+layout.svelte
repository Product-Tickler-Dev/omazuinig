<script lang="ts">
  import '../app.css';
  import BottomNav from '$lib/components/BottomNav.svelte';
  import Toast from '$lib/components/Toast.svelte';

  let { children } = $props();
</script>

<div class="app-shell">
  {@render children()}
  <BottomNav />
  <Toast />
</div>

<style>
  .app-shell {
    max-width: 480px;
    margin: 0 auto;
    min-height: 100vh;
    position: relative;
  }
</style>
