<script>
  import Navbar from "./lib/components/Navbar/Navbar.svelte";
  import Router, { replace as replaceRoute } from "svelte-spa-router";
  import routes from "./routes/";
  import { getUserData, setupUserSettings } from "./lib/functions/user"
  let ready = false;

  function prepareApp() {
    setupUserSettings();
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
  <!--<Footer />-->
{/if}
