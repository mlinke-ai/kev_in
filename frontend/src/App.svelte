<script>
  import Navbar from "./lib/components/Navbar/Navbar.svelte";
  import Router from "svelte-spa-router";
  import routes from "./routes/";
</script>

<Navbar />
<Router {routes} />
