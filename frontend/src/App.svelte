<script>
  import Navbar from "./lib/components/Navbar/Navbar.svelte";
  import Router, { replace as replaceRoute } from "svelte-spa-router";
  import routes from "./routes/";
  import { setupUserSettings, getAccessLevel } from "./lib/functions/user";
  import { startPage } from "./stores";

  let ready = false;

  function prepareApp() {
    setupUserSettings(getAccessLevel())
    // replaceRoute($startPage);
    ready = true;
  }
</script>

<svelte:window
  on:load={() => {
    prepareApp();
  }}
/>

{#if ready}
  <!--<Navbar />-->
  <Router {routes} />
{:else}
  preparing...
{/if}