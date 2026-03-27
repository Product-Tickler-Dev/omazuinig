<script lang="ts">
  let { categories, active, onselect }: {
    categories: string[];
    active: string;
    onselect: (cat: string) => void;
  } = $props();
</script>

<div class="pills">
  {#each categories as cat}
    <button
      class="pill"
      class:active={cat === active}
      onclick={() => onselect(cat)}
    >
      {cat}
    </button>
  {/each}
</div>

<style>
  .pills {
    display: flex;
    gap: 6px;
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
    padding: 5px 14px;
    border-radius: var(--radius-full);
    border: 1.5px solid var(--blue);
    background: transparent;
    color: var(--blue);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
    text-transform: capitalize;
  }

  .pill.active {
    background: var(--blue);
    color: white;
    border-color: var(--blue);
  }

  .pill:hover:not(.active) {
    background: var(--blue-light);
  }
</style>
