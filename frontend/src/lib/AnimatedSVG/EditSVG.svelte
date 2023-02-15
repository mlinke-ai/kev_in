<script>
    import { draw } from "svelte/transition";
    import { quintOut } from "svelte/easing";
  
    export let delayAnimation = 250;
</script>

<svg
  focusable="false"
  aria-hidden="true"
  viewBox="-2 -2 4 4"
  ><path
  in:draw={{ duration: 100, easing: quintOut, delay: delayAnimation }}
    fill="none"
    stroke="#5382a1"
    stroke-width="0.3px"
    d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a.9959.9959 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"
  /></svg
>
