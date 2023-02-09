<!-- Skeletton component for all pages to provide 
    unified transitions, title naming and basic access control 
-->
<script>
  import { blur } from "svelte/transition";
  import { accessLevel } from "../../../stores";
  import { accessLevels } from "../../constants";
  import { replace as replaceRoute } from "svelte-spa-router";

  export let transition = true;
  export let title = "";
  export let requiredAccessLevel = accessLevels.default;
  export let fullwidth = false;

  if ($accessLevel < requiredAccessLevel) {
    replaceRoute("/access-denied");
  }
</script>

<svelte:head>
  {#if title}
    <title>Kev.In - {title}</title>
  {:else}
    <title>Kev.In</title>
  {/if}
</svelte:head>

{#if transition}
  <div class="page" in:blur={{ duration: 250 }}>
    <slot />
  </div>
{:else}
  <div class="page">
    <slot />
  </div>
{/if}

{#if fullwidth}
  <style>
    body {
      margin: 0;
      background: rgb(0, 57, 49);
      background: radial-gradient(
        circle,
        rgba(0, 57, 49, 1) 0%,
        rgba(0, 20, 17, 1) 100%
      );
    }
    .page {
      margin: 0;
      padding: 0;
    }
  </style>
{:else}
  <style>
    body {
      margin: 0;
    }
    .page {
      margin: 7rem 5rem 7rem 5rem;
    }
  </style>
{/if}
