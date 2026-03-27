<script lang="ts">
  import { page } from '$app/stores';

  const links = [
    { href: '/', icon: '\u{1F3E0}', label: 'Home' },
    { href: '/lijst', icon: '\u{1F4DD}', label: 'Lijst' },
    { href: '/vergelijk', icon: '\u{1F50D}', label: 'Vergelijk' },
    { href: '/deals', icon: '\u{1F525}', label: 'Deals' },
    { href: '/mijn-oma', icon: '\u{1F475}', label: 'Mijn Oma' }
  ];
</script>

<nav class="bottom-nav">
  {#each links as link}
    <a
      href={link.href}
      class="nav-link"
      class:active={$page.url.pathname === link.href}
    >
      <span class="icon">{link.icon}</span>
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
    box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.08);
    padding: 6px 0;
    padding-bottom: max(6px, env(safe-area-inset-bottom));
    z-index: 100;
  }

  .nav-link {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
    color: #999;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 8px;
    transition: color 0.2s;
  }

  .nav-link.active {
    color: var(--orange);
  }

  .icon {
    font-size: 22px;
    line-height: 1;
  }

  .label {
    margin-top: 2px;
  }
</style>
