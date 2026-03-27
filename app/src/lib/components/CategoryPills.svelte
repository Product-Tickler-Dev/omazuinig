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
    gap: 8px;
    overflow-x: auto;
    padding: 8px 0;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .pills::-webkit-scrollbar {
    display: none;
  }

  .pill {
    flex-shrink: 0;
    padding: 6px 16px;
    border-radius: 999px;
    border: 2px solid var(--orange);
    background: white;
    color: var(--dark);
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
  }

  .pill.active {
    background: var(--orange);
    color: white;
  }

  .pill:hover:not(.active) {
    background: #fff3e0;
  }
</style>
