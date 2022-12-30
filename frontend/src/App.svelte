<script>
  import Navbar from "./lib/components/Navbar/Navbar.svelte";
  import Router from "svelte-spa-router";
  import routes from "./routes/";
  import { userLoggedIn, startPage } from "./stores";

  function isAuthenticated() {
    return true;
  }
</script>

<svelte:window
  on:load={() => {
    if (isAuthenticated()) {
      $userLoggedIn = true;
      $startPage = "#/profile"
    }
  }}
/>

<Navbar />
<Router {routes} />
