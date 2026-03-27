<script lang="ts">
  let { text }: { text: string } = $props();
</script>

<div class="bubble-wrapper">
  <div class="avatar">&#x1F475;</div>
  <div class="bubble">
    <p class="oma-text">{text}</p>
  </div>
</div>

<style>
  .bubble-wrapper {
    display: flex;
    align-items: flex-start;
    gap: var(--space-3);
    padding: var(--space-3) 0;
    animation: fadeSlideIn 0.4s ease-out;
  }

  .avatar {
    font-size: 24px;
    flex-shrink: 0;
    line-height: 1;
    padding-top: 2px;
  }

  .bubble {
    background: #FFF5E6;
    border-left: 3px solid var(--orange);
    border-radius: var(--radius-sm);
    padding: var(--space-3) var(--space-4);
  }

  .oma-text {
    font-family: 'Caveat', cursive;
    font-weight: 700;
    font-size: 18px;
    color: var(--dark);
    line-height: 1.3;
  }
</style>
