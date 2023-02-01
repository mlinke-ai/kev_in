<script>
  import Navbar from "./lib/components/Navbar/Navbar.svelte";
  import Router from "svelte-spa-router";
  import routes from "./routes/";
  import { setupUserSettings } from "./lib/functions/user";
  import { accessLevel } from "./stores";

  function prepareApp() {
    setupUserSettings();
  }
</script>

<svelte:window
  on:load={() => {
    prepareApp();
  }}
/>

{#if $accessLevel >= 0}
  <Navbar />
  <Router {routes} />
  <!--<Footer />-->
{/if}
