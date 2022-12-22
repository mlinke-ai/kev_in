<script>
  import Card, { Media } from "@smui/card/";
  import Ripple from "@smui/ripple";
  import PythonSvg from "./AnimatedSVG/PythonSVG.svelte";
  import { fade } from "svelte/transition";

  export let title = ""
  export let description = ""

  let showText = false;

</script>

<div
  class="language-card"
  use:Ripple={{ surface: true, color: "primary", unbounded: true }}
>
  <Card
    style="border-radius:40px; width: 400px;"
    variant="outlined"
    on:mouseenter={() => (showText = true)}
    on:mouseleave={() => (showText = false)}
  >
    <Media>
        <slot />
    </Media>
    {#if showText}
      <div class="language-card-text-area" in:fade>
        <h2 class="mdc-typography--headline6" style="margin: 0;">{title}</h2>
        <h3 class="mdc-typography--subtitle2" style="margin: 0;">
          {description}
        </h3>
      </div>
    {/if}
  </Card>
</div>

<style>
  .language-card-text-area {
    color: #ccc;
    position: absolute;
    bottom: 16px;
    left: 16px;
  }
  .language-card {
    margin: 5px;
  }
</style>
