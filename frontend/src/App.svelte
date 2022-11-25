<script>
    import { Router, Route } from "svelte-routing"
    import Demo from "./routes/demo.svelte"

    let url=""
</script>

<Router url="{url}">
    <main>
      <!--<Route path="/example" component="{Example}" />-->
      <Route path="/"><Demo /></Route>
    </main>
</Router>