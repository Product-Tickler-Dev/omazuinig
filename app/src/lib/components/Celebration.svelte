<script lang="ts">
  import { toasts } from '$lib/stores/toast';

  let celebrations = $derived($toasts.filter(t => t.type === 'celebrate'));
</script>

{#each celebrations as toast (toast.id)}
  <div class="celebration" role="status" aria-live="polite">
    <div class="confetti-container">
      <span class="confetti c1"></span>
      <span class="confetti c2"></span>
      <span class="confetti c3"></span>
    </div>
    <div class="celebration-content">
      <img src="/oma-avatar.png" alt="" class="cele-avatar" />
      <span class="cele-text">{toast.text} Bespaar &euro;{toast.amount?.toFixed(2).replace('.', ',')}</span>
    </div>
  </div>
{/each}

<style>
  .celebration {
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 480px;
    background: linear-gradient(135deg, #00C853 0%, #00913B 100%);
    color: white;
    padding: 14px 20px;
    z-index: 210;
    animation: celebrateIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    overflow: hidden;
  }

  @keyframes celebrateIn {
    from {
      transform: translateX(-50%) scale(0.95);
      opacity: 0;
    }
    to {
      transform: translateX(-50%) scale(1);
      opacity: 1;
    }
  }

  .celebration-content {
    display: flex;
    align-items: center;
    gap: 10px;
    position: relative;
    z-index: 2;
  }

  .cele-avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    object-fit: cover;
    flex-shrink: 0;
    border: 2px solid rgba(255, 255, 255, 0.6);
  }

  .cele-text {
    font-size: 14px;
    font-weight: 600;
    line-height: 1.3;
  }

  .confetti-container {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
    overflow: hidden;
  }

  .confetti {
    position: absolute;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    animation: confettiFloat 1.2s ease-out forwards;
  }

  .c1 {
    background: #FFD700;
    left: 20%;
    bottom: 0;
    animation-delay: 0.1s;
  }

  .c2 {
    background: #FF8A3D;
    left: 55%;
    bottom: 0;
    animation-delay: 0.25s;
  }

  .c3 {
    background: #FFFFFF;
    left: 80%;
    bottom: 0;
    animation-delay: 0.4s;
  }

  @keyframes confettiFloat {
    0% {
      transform: translateY(0) scale(1);
      opacity: 1;
    }
    100% {
      transform: translateY(-40px) scale(0.3);
      opacity: 0;
    }
  }
</style>
