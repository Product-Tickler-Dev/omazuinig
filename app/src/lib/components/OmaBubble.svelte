<script lang="ts">
  type Mood = 'happy' | 'excited' | 'thinking' | 'neutral' | 'wink' | 'sad' | 'proud';

  let { text, mood = 'happy' }: { text: string; mood?: Mood } = $props();

  const moodImages: Record<Mood, string> = {
    happy: '/oma-avatar.png',
    neutral: '/oma-avatar.png',
    excited: '/oma-excited.webp',
    thinking: '/oma-thinking.webp',
    wink: '/oma-wink.webp',
    sad: '/oma-sad.webp',
    proud: '/oma-proud.webp'
  };

  let imageSrc = $derived(moodImages[mood] ?? '/oma-avatar.png');
</script>

<div class="bubble-wrapper">
  <div class="avatar-ring" class:mood-change={mood !== 'happy' && mood !== 'neutral'}>
    {#key imageSrc}
      <img src={imageSrc} alt="Oma Zuinig" class="avatar-img" />
    {/key}
  </div>
  <div class="bubble">
    <div class="bubble-tail"></div>
    <p class="oma-text">
      {text}{#if mood === 'thinking'}<span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span>{/if}
    </p>
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
    width: 56px;
    height: 56px;
    border-radius: 50%;
    padding: 2px;
    background: linear-gradient(135deg, var(--orange) 0%, var(--orange-warm, #FF8A3D) 100%);
    box-shadow: 0 4px 12px rgba(255, 98, 0, 0.2);
  }

  .avatar-ring.mood-change {
    animation: avatarPop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  @keyframes avatarPop {
    0% { transform: scale(0.8); }
    50% { transform: scale(1.08); }
    100% { transform: scale(1); }
  }

  .avatar-img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    display: block;
    animation: imgFadeIn 0.3s ease-out;
  }

  @keyframes imgFadeIn {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
  }

  .bubble {
    position: relative;
    background: #F8F5F0;
    padding: var(--space-3) var(--space-4);
    animation: bubbleSlide 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  @keyframes bubbleSlide {
    from { opacity: 0; transform: translateX(-8px); }
    to { opacity: 1; transform: translateX(0); }
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

  .thinking-dots span {
    animation: dotPulse 1.4s ease-in-out infinite;
    display: inline-block;
  }

  .thinking-dots span:nth-child(2) {
    animation-delay: 0.2s;
  }

  .thinking-dots span:nth-child(3) {
    animation-delay: 0.4s;
  }

  @keyframes dotPulse {
    0%, 60%, 100% { opacity: 0.3; }
    30% { opacity: 1; }
  }
</style>
