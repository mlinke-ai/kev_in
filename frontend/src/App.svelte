<script>
  import Navbar from "./lib/Navbar/Navbar.svelte";
  import Router from "svelte-spa-router";
  import routes from "./routes/";
  import { setupUserSettings } from "./lib/Authentication/user";
  import { accessLevel } from "./stores";
  import AcceptCookies from "./lib/AcceptCookies/AcceptCookies.svelte";

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
