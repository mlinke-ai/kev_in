<script>
    import { Router, Route } from "svelte-routing"
    import Login from "./routes/login.svelte";

    let url=""
</script>

<Router url="{url}">
    <main>
     <Route path="/auth" component="{Login}" />
    </main>
</Router>