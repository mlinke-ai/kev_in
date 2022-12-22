<!-- Component for animated language cards with media background -->

<script>
  import Card, { Media } from "@smui/card/";
  import Ripple from "@smui/ripple";
  import { fade } from "svelte/transition";

  export let title = "";
  export let description = "";

  let showText = false;
  let blurMedia = false;
</script>

<div
  use:Ripple={{ surface: true, color: "primary", unbounded: true }}
>
  <Card
    class="language-card"
    variant="outlined"
    on:mouseenter={() => (showText = true)}
    on:mouseleave={() => (showText = false)}
    on:mouseenter={() => (blurMedia = true)}
    on:mouseleave={() => (blurMedia = false)}
  >
    <Media>
      <div class:blur={blurMedia} class:unblur={!blurMedia}>
        <slot />
      </div>
    </Media>
    {#if showText}
      <div class="language-card-title" transition:fade>
        <h2 class="mdc-typography--headline6" style="margin: 0;">{title}</h2>
      </div>
      <div class="language-card-description" transition:fade>
        <h3 class="mdc-typography--subtitle2" style="margin: 0;">
          {description}
        </h3>
      </div>
    {/if}
  </Card>
</div>

<style>
  * :global(.language-card) {
    border-radius: 40px;
    width: 400px;
    height: 400px;
    box-sizing: border-box;
  }

  .language-card-description {
    color: #ccc;
    position: absolute;
    bottom: 16px;
    text-align: center;
    padding: 0.5rem;
  }
  .language-card-title {
    color: #ccc;
    position: absolute;
    top: 16px;
    left: 16px;
  }

  .blur {
    animation: blur 1s;
    -webkit-animation: blur 1s;
    animation-fill-mode: forwards;
  }

  .unblur {
    animation: unblur 1s;
    -webkit-animation: unblur 1s;
    animation-fill-mode: forwards;
  }

  @keyframes blur {
    0% {
      -webkit-filter: blur(0px);
    }
    100% {
      -webkit-filter: blur(.5rem);
    }
  }

  @keyframes unblur {
    0% {
      -webkit-filter: blur(.5rem);
    }
    100% {
      -webkit-filter: blur(0px);
    }
  }
</style>
