<script>
    import { Router, Route } from "svelte-routing"
    import Navbar from "./lib/components/Navbar/Navbar.svelte"
    import Login from "./routes/login.svelte";
    import Home from "./routes/home.svelte"

    let url=""
</script>

<Router url="{url}">
  <Navbar />
  <main>
    <main>
     <Route path="/auth" component="{Login}" />
      <!--<Route path="/example" component="{Example}" />-->
      <Route path="/"><Home /></Route>
    </main>
  </main>
</Router>

<style>
  main {
    margin-top: 5rem;
  }
</style>