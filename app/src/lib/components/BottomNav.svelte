<script lang="ts">
  import { page } from '$app/stores';

  const links = [
    { href: '/', label: 'Home', icon: 'home' },
    { href: '/lijst', label: 'Lijst', icon: 'lijst' },
    { href: '/vergelijk', label: 'Vergelijk', icon: 'vergelijk' },
    { href: '/deals', label: 'Deals', icon: 'deals' },
    { href: '/mijn-oma', label: 'Mijn Oma', icon: 'mijnoma' }
  ];
</script>

<nav class="bottom-nav" aria-label="Hoofdnavigatie">
  {#each links as link}
    <a
      href={link.href}
      class="nav-link"
      class:active={$page.url.pathname === link.href}
      aria-current={$page.url.pathname === link.href ? 'page' : undefined}
    >
      <span class="icon-wrap" class:icon-active={$page.url.pathname === link.href}>
        {#if link.icon === 'home'}
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z"/>
            <path d="M9 21V12h6v9"/>
          </svg>
        {:else if link.icon === 'lijst'}
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <path d="M8 8h8M8 12h8M8 16h5"/>
          </svg>
        {:else if link.icon === 'vergelijk'}
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M8 3v18M16 3v18"/>
            <path d="M3 8h5M16 8h5"/>
            <path d="M3 16h5M16 16h5"/>
          </svg>
        {:else if link.icon === 'deals'}
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/>
            <circle cx="7" cy="7" r="1.5"/>
          </svg>
        {:else if link.icon === 'mijnoma'}
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
          </svg>
        {/if}
      </span>
      <span class="label">{link.label}</span>
    </a>
  {/each}
</nav>

<style>
  .bottom-nav {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 480px;
    display: flex;
    justify-content: space-around;
    background: white;
    border-top: 1px solid var(--gray-200);
    padding: 6px 0;
    padding-bottom: max(6px, env(safe-area-inset-bottom));
    z-index: 100;
    height: 64px;
  }

  .nav-link {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
    color: var(--gray-400);
    font-size: 11px;
    font-weight: 500;
    padding: 4px 14px;
    justify-content: center;
    gap: 3px;
    position: relative;
    transition: color var(--transition-fast);
    -webkit-tap-highlight-color: transparent;
  }

  .nav-link:active .icon-wrap {
    transform: scale(0.9);
  }

  .nav-link.active {
    color: var(--orange);
    font-weight: 600;
  }

  .icon-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 44px;
    border-radius: var(--radius-full);
    transition: all var(--transition-fast);
  }

  .icon-wrap.icon-active {
    background: var(--orange-light);
    transform: scale(1);
  }

  .icon-wrap.icon-active svg {
    stroke: var(--orange);
    stroke-width: 2.5;
  }

  .label {
    letter-spacing: 0.01em;
    line-height: 1;
  }

  @media (min-width: 768px) {
    .bottom-nav {
      display: none;
    }
  }
</style>
