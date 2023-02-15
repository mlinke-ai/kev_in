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
    d="M5 5h2v3h10V5h2v5h2V5c0-1.1-.9-2-2-2h-4.18C14.4 1.84 13.3 1 12 1s-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h6v-2H5V5zm7-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1z"
  /><path 
  in:draw={{ duration: 1000, easing: quintOut, delay: delayAnimation }}
    fill="none"
    stroke="#5382a1"
    stroke-width="0.3px"
  d="M21 11.5 15.51 17l-3.01-3-1.5 1.5 4.51 4.5 6.99-7z" /></svg
>
