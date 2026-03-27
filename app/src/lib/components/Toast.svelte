<script lang="ts">
  import { toasts } from '$lib/stores/toast';
</script>

{#each $toasts as toast (toast.id)}
  <div class="toast" role="status" aria-live="polite">
    <img src="/oma-avatar.png" alt="" class="toast-avatar" />
    <span class="toast-text">{toast.text}</span>
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
    padding: 10px 20px 10px 10px;
    border-radius: var(--radius-full);
    box-shadow: var(--shadow-lg);
    font-size: 14px;
    font-weight: 500;
    z-index: 200;
    animation: slideDown 0.3s ease-out;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .toast-avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    object-fit: cover;
    flex-shrink: 0;
  }

  .toast-text {
    line-height: 1.3;
  }
</style>
