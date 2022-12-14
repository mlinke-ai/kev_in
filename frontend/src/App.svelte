<script>
    import { Router, Route } from "svelte-routing"
    import Demo from "./routes/demo.svelte"
    import Home from "./routes/home.svelte"

    let url=""
</script>

<Router url="{url}">
    <main>
      <!--<Route path="/example" component="{Example}" />-->
      <Route path="/"><Demo /></Route>
      <Route path="/home"><Home></Home></Route>
    </main>
</Router>