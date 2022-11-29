<script>
    import { Link } from "svelte-routing"
    import { Icon } from "@smui/button"
    import Ripple from "@smui/ripple"

    export let label = ""
    export let route = "/"
    export let icon = ""
</script>

<li class="navbar-item">
    <Link to={route}>
        <div class="navbar-link" use:Ripple={{ surface: true, color: "primary"}}>
            <!--<Icon class="material-icons">{icon}</Icon>-->
            {label}
        </div>
    </Link>
</li>

<style>
    .navbar-item {
        list-style-type: none;
        background-color: none;
        display: flex;
        align-items: center;
        text-transform: uppercase;
        position:relative;
        margin: 0;
        height: 100%;
    }

    .navbar-item:hover::after {
        content: "_";
        position: absolute;
        right: .5rem;
        animation: blink 1s linear infinite;
    }

    @keyframes blink {
        50% {
            opacity: 0;
        }
    }

    .navbar-link {
        padding: 1rem;
    }
</style>