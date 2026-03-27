<script lang="ts">
  import { toasts } from '$lib/stores/toast';
</script>

{#each $toasts as toast (toast.id)}
  <div class="toast">
    {toast.text}
  </div>
{/each}

<style>
  .toast {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--dark);
    color: white;
    padding: 10px 24px;
    border-radius: var(--radius-full);
    box-shadow: var(--shadow-md);
    font-size: 14px;
    font-weight: 500;
    z-index: 200;
    animation: slideDown 0.3s ease-out;
    white-space: nowrap;
  }
</style>
