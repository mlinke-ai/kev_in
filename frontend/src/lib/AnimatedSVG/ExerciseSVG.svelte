<script>
  import { draw } from "svelte/transition";
  import { quintOut } from "svelte/easing";

  export let delayAnimation = 250;
</script>

<svg focusable="false" aria-hidden="true" viewBox="0 0 24 24"
  ><path
    in:draw={{ duration: 10000, easing: quintOut, delay: delayAnimation }}
    fill="none"
    stroke="#5382a1"
    stroke-width="0.3px"
    d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9H9V9h10v2zm-4 4H9v-2h6v2zm4-8H9V5h10v2z"
  /></svg
>
