<script>
  import { draw } from "svelte/transition";
  import { quintOut } from "svelte/easing";

  export let delayAnimation = 250;
</script>

<svg focusable="false" aria-hidden="true" viewBox="-3 -2 30 30"
  ><path
    in:draw={{ duration: 10000, easing: quintOut, delay: delayAnimation }}
    fill="none"
    stroke="#5382a1"
    stroke-width="0.3px"
    d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
  />
</svg>
