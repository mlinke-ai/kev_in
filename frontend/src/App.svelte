<script>
    import { Router, Route } from "svelte-routing"
    import Login from "./routes/login.svelte";
    import Home from "./routes/home.svelte"

    let url=""
</script>

<Router url="{url}">
    <main>
     <Route path="/auth" component="{Login}" />
      <!--<Route path="/example" component="{Example}" />-->
      <Route path="/"><Home /></Route>
    </main>
</Router>