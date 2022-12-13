<script>
    import { Router, Route } from "svelte-routing"

    import Navbar from "./lib/components/Navbar/Navbar.svelte"

    let url=""
</script>

<Router url="{url}">
  <Navbar />
  <main>
    <!--<Route path="/example" component="{Example}" />-->
  </main>
</Router>

<style>
  main {
    margin-top: 5rem;
  }
</style>