<script>
    import { Router, Route } from "svelte-routing"
    import Demo from "./routes/demo.svelte"
    import Error from "./routes/error.svelte"

    let url=""
</script>

<Router url="{url}">
    <main>
      <!--<Route path="/example" component={Example} />-->
      <Route path="/error" component={Error} />
      <Route path="/"><Demo /></Route>
    </main>
</Router>