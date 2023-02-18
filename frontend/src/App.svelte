<script>
  import Navbar from "./lib/Navbar/Navbar.svelte";
  import Router from "svelte-spa-router";
  import routes from "./routes/";
  import { getUser, storeUser } from "./lib/Authentication/user";
  import { accessLevel } from "./stores";
  import AcceptCookies from "./lib/AcceptCookies/AcceptCookies.svelte";
  import { accessLevels } from "./lib/constants";

  const prepareApp = async () => {
    const user = await getUser();
    console.log(user)
    if(user) {
      storeUser(user)
    } else {
      $accessLevel = accessLevels.default;
    }
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
