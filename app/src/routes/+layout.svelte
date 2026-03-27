<script lang="ts">
  import '../app.css';
  import { page } from '$app/stores';
  import { fade } from 'svelte/transition';
  import BottomNav from '$lib/components/BottomNav.svelte';
  import Toast from '$lib/components/Toast.svelte';
  import Celebration from '$lib/components/Celebration.svelte';

  let { children } = $props();
</script>

<div class="app-shell">
  {#key $page.url.pathname}
    <div class="page-transition" transition:fade={{ duration: 150 }}>
      {@render children()}
    </div>
  {/key}
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

  .page-transition {
    min-height: 100vh;
  }
</style>
