<script lang="ts">
  import { toasts } from '$lib/stores/toast';
</script>

{#each $toasts as toast (toast.id)}
  <div class="toast" class:info={toast.type === 'info'}>
    {toast.text}
  </div>
{/each}

<style>
  .toast {
    position: fixed;
    top: 16px;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    color: var(--dark);
    padding: 12px 20px;
    border-radius: var(--radius-sm);
    box-shadow: var(--shadow-lg);
    border-left: 4px solid var(--green);
    font-size: 14px;
    font-weight: 700;
    z-index: 200;
    animation: slideDown 0.3s ease-out;
  }

  .toast.info {
    border-left-color: var(--blue);
  }
</style>
