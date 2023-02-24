<!-- Skeletton component for all pages to provide 
    unified transitions, title naming and basic access control 
-->
<script lang="ts">
  import { blur, slide } from "svelte/transition";
  import { accessLevel } from "../../stores";
  import { accessLevels } from "./types";
  import { replace as replaceRoute } from "svelte-spa-router";

  export let blurTransition = true;
  export let slideTransition = false;
  export let title = "";
  export let requiredAccessLevel: accessLevels = accessLevels.default;
  export let fullwidth = false;

  if ($accessLevel < requiredAccessLevel) {
    replaceRoute("/");
  }
</script>

<svelte:head>
  {#if title}
    <title>Kev.In - {title}</title>
  {:else}
    <title>Kev.In</title>
  {/if}
</svelte:head>
{#if slideTransition}
  <div class="page" in:slide={{ duration: 500 }}>
    <slot />
  </div>
{:else if blurTransition}
  <div class="page" in:blur={{ duration: 500 }}>
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
      overflow: overlay;
    }
    .page {
      margin: 0rem 0rem 0rem 0rem;
      padding: 0;
    }
  </style>
{:else}
  <style>
    body {
      margin: 0;
      overflow: overlay;
    }
    .page {
      margin: 7rem 5rem 7rem 5rem;
    }
  </style>
{/if}
