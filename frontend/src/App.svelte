<script>
    import { Router, Route } from "svelte-routing"

    import Navbar from "./lib/components/Navbar/Navbar.svelte"
    import Demo from "./routes/demo.svelte"
    import Login from "./routes/login.svelte"
    import Lecture from "./routes/lecture.svelte"
    import Register from "./routes/register.svelte"

    let url=""
</script>

<Router url="{url}">
  <Navbar />
  <main>
    <!--<Route path="/example" component="{Example}" />-->
    <Route path="/login"><Login /></Route>
    <Route path="/register"><Register /></Route>
    <Route path="/lecture"><Lecture /></Route>
    <Route path="/"><Demo /></Route>
  </main>
</Router>

<style>
  main {
    margin-top: 5rem;
  }
</style>