<script>
    import { Link } from "svelte-routing";
    import Button from "@smui/button";
    
    export let label = ""
    export let route = ""
    export let variant = ""
</script>

<div class="navbar-button">
    <Link to={route}>
        <Button variant={variant}>{label}</Button>
    </Link>
</div>

<style>
    .navbar-button {
        margin-left: 1rem;
    }
</style>