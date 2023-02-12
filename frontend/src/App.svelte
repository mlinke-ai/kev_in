<script>
  import Navbar from "./lib/components/Navbar/Navbar.svelte";
  import Router from "svelte-spa-router";
  import routes from "./routes/";
  import { setupUserSettings } from "./lib/functions/user";
  import { accessLevel } from "./stores";
  import AcceptCookies from "./lib/components/AcceptCookies/AcceptCookies.svelte";

  const prepareApp = async () => {
    await setupUserSettings().then(null, () => {
      $accessLevel = 0;
    });
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
  <AcceptCookies />
{/if}
