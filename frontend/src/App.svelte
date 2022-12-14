<script>
    import { Router, Route } from "svelte-routing"
    import Error from "./routes/error.svelte"
  import Navbar from "./lib/components/Navbar/Navbar.svelte";
  import Login from "./routes/login.svelte";
  import Home from "./routes/home.svelte";

  let url = "";
</script>

<Router {url}>
  <Navbar />
  <main>
    <Route path="/auth" component={Login} />
    <!--<Route path="/example" component="{Example}" />-->
    <Route path="/"><Home /></Route>
    <Route path="/error" component={Error} />
  </main>
</Router>

<style>
  main {
    margin-top: 5rem;
  }
</style>

