<script>
  import Navbar from "./lib/components/Navbar/Navbar.svelte";
  import Router from "svelte-spa-router";
  import routes from "./routes/";
</script>

<Navbar />
<main>
    <Router {routes} />
</main>

<style>
  main {
    padding: 5rem;
  }
</style>
