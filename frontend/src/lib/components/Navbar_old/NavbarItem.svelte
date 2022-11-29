<script>
    import { Link } from "svelte-routing"

    export let label = ""
    export let route = "/"
    export let icon = ""
</script>

<li class="navbar-item">
    <Link to={route}>
        {label}
    </Link>
</li>

<style>
    .navbar-item {
        list-style-type: none;
        padding-left: 1rem;
        padding-right: 1rem;
        font-family: "Roboto";
    }
</style>