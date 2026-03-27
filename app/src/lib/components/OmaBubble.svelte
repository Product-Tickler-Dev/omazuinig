<script lang="ts">
  let { text }: { text: string } = $props();
</script>

<div class="bubble-wrapper">
  <div class="avatar-ring">
    <img src="/oma-avatar.png" alt="Oma Zuinig" class="avatar-img" />
  </div>
  <div class="bubble">
    <div class="bubble-tail"></div>
    <p class="oma-text">{text}</p>
  </div>
</div>

<style>
  .bubble-wrapper {
    display: flex;
    align-items: flex-start;
    gap: var(--space-3);
    padding: var(--space-3) 0;
    animation: bounceIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .avatar-ring {
    flex-shrink: 0;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    padding: 2px;
    background: linear-gradient(135deg, var(--orange) 0%, var(--orange-warm, #FF8A3D) 100%);
    box-shadow: 0 4px 12px rgba(255, 98, 0, 0.2);
  }

  .avatar-img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    display: block;
  }

  .bubble {
    position: relative;
    background: white;
    border: 2px solid var(--orange-light);
    border-radius: var(--radius-lg);
    padding: var(--space-3) var(--space-4);
    box-shadow: 0 2px 8px rgba(255, 98, 0, 0.08);
  }

  .bubble-tail {
    position: absolute;
    left: -8px;
    top: 16px;
    width: 0;
    height: 0;
    border-top: 6px solid transparent;
    border-bottom: 6px solid transparent;
    border-right: 8px solid white;
    filter: drop-shadow(-2px 0 1px rgba(255, 98, 0, 0.06));
  }

  .bubble-tail::before {
    content: '';
    position: absolute;
    left: -1px;
    top: -8px;
    width: 0;
    height: 0;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
    border-right: 10px solid var(--orange-light);
    z-index: -1;
  }

  .oma-text {
    font-family: 'Caveat', cursive;
    font-weight: 700;
    font-size: 21px;
    color: var(--dark);
    line-height: 1.3;
  }
</style>
