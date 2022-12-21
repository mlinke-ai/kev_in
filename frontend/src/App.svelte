<script>
  import Router from "svelte-spa-router";
  import routes from "./routes/";

  import Navbar from "./lib/components/Navbar/Navbar.svelte";

  let url = "";
</script>

<Navbar />
<main>
  <Router {routes} />
</main>

<style>
  main {
    margin-top: 5rem;
  }
</style>
