<script>
  import Navbar from "./lib/components/Navbar/Navbar.svelte";
  import Router, { replace as replaceRoute } from "svelte-spa-router";
  import routes from "./routes/";
  import { userLoggedIn, startPage } from "./stores";

  let ready = false;

  function isAuthenticated() {
    return true;
  }
</script>

<svelte:window
  on:load={() => {
    if (isAuthenticated()) {
      $userLoggedIn = true;
      $startPage = "#/profile";
    }
    replaceRoute($startPage);
    ready = true
  }}
/>

{#if ready}
  <Navbar />
  <Router {routes} />
{/if}
