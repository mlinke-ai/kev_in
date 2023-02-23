<!-- Skeletton component for all pages to provide 
    unified transitions, title naming and basic access control 
-->
<script lang="ts">
  import { blur } from "svelte/transition";
  import { replace as replaceRoute } from "svelte-spa-router";
  import { renderNavbar } from "../../stores";

  export let transition = true;
  export let title = "";
  export let fullwidth = false;

  $renderNavbar = !fullwidth;
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
