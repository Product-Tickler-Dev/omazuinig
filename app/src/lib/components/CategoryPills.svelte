<script lang="ts">
  let { categories, active, onselect }: {
    categories: string[];
    active: string;
    onselect: (cat: string) => void;
  } = $props();
</script>

<div class="pills" role="group" aria-label="Filter op categorie">
  {#each categories as cat}
    <button
      class="pill"
      class:active={cat === active}
      aria-pressed={cat === active}
      onclick={() => onselect(cat)}
    >
      {cat}
    </button>
  {/each}
</div>

<style>
  .pills {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 4px 0;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .pills::-webkit-scrollbar {
    display: none;
  }

  .pill {
    flex-shrink: 0;
    padding: 12px 18px;
    border-radius: var(--radius-full);
    border: 2px solid var(--blue);
    background: transparent;
    color: var(--blue);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition-fast);
    text-transform: capitalize;
    -webkit-tap-highlight-color: transparent;
  }

  .pill:active {
    transform: scale(0.95);
  }

  .pill.active {
    background: var(--blue);
    color: white;
    border-color: var(--blue);
    box-shadow: 0 4px 12px rgba(0, 82, 204, 0.2);
  }

  .pill:hover:not(.active) {
    background: var(--blue-light);
  }
</style>
