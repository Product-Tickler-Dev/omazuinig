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
    gap: 12px;
    padding: 12px;
  }

  .avatar {
    font-size: 40px;
    flex-shrink: 0;
  }

  .bubble {
    background: var(--cream);
    border: 2px solid var(--orange);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    position: relative;
    box-shadow: var(--shadow-sm);
  }

  .bubble::before {
    content: '';
    position: absolute;
    left: -8px;
    top: 12px;
    width: 0;
    height: 0;
    border-top: 6px solid transparent;
    border-bottom: 6px solid transparent;
    border-right: 8px solid var(--orange);
  }

  .oma-text {
    font-family: 'Caveat', cursive;
    font-size: 20px;
    color: var(--dark);
    line-height: 1.3;
  }
</style>
