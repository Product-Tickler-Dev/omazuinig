<script lang="ts">
  import { page } from '$app/stores';

  const links = [
    { href: '/', label: 'Home' },
    { href: '/lijst', label: 'Lijst' },
    { href: '/vergelijk', label: 'Vergelijk' },
    { href: '/deals', label: 'Deals' },
    { href: '/mijn-oma', label: 'Mijn Oma' }
  ];
</script>

<nav class="desktop-nav" aria-label="Hoofdnavigatie">
  <div class="nav-inner">
    <a href="/" class="nav-brand">
      <img src="/oma-avatar.png" alt="" class="nav-oma" />
      <span class="nav-title">Oma Zuinig</span>
    </a>
    <div class="nav-links">
      {#each links as link}
        <a
          href={link.href}
          class="nav-item"
          class:active={$page.url.pathname === link.href}
          aria-current={$page.url.pathname === link.href ? 'page' : undefined}
        >
          {link.label}
        </a>
      {/each}
    </div>
    <div class="nav-right"></div>
  </div>
</nav>

<style>
  .desktop-nav {
    display: none;
    position: sticky;
    top: 0;
    z-index: 100;
    background: white;
    border-bottom: 1px solid var(--gray-200);
  }

  @media (min-width: 768px) {
    .desktop-nav {
      display: block;
    }
  }

  .nav-inner {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    height: 64px;
    padding: 0 var(--space-8);
    gap: var(--space-8);
  }

  .nav-brand {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    text-decoration: none;
    flex-shrink: 0;
  }

  .nav-oma {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    object-fit: cover;
  }

  .nav-title {
    font-size: 22px;
    font-weight: 700;
    color: var(--orange);
    letter-spacing: -0.02em;
  }

  .nav-links {
    display: flex;
    align-items: center;
    gap: var(--space-1);
  }

  .nav-item {
    padding: var(--space-2) var(--space-4);
    text-decoration: none;
    font-size: 15px;
    font-weight: 600;
    color: var(--gray-600);
    border-radius: var(--radius-lg);
    transition: all var(--transition-fast);
  }

  .nav-item:hover {
    color: var(--dark);
    background: var(--gray-50);
  }

  .nav-item.active {
    color: var(--orange);
    background: var(--orange-light);
  }

  .nav-right {
    margin-left: auto;
  }
</style>
