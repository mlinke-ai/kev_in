<script>
    import Ripple from "@smui/ripple";
    import { onMount } from "svelte";
    import { blur } from "svelte/transition";

    export let label = "";
    export let route = "/";
    export let id = 0;
    let ready = false

    onMount(() => {
        ready = true
    })
</script>

{#if ready}
<li class="navbar-item" in:blur="{{ duration: 250, delay: (id + 1) * 250 }}">
    <a href={route}>
        <div
            class="navbar-link"
            use:Ripple={{ surface: true, color: "primary" }}
        >
            {label}
        </div>
    </a>
</li>
{/if}

<style>
    .navbar-item {
        list-style-type: none;
        background-color: none;
        display: flex;
        align-items: center;
        text-transform: uppercase;
        position: relative;
        margin: 0;
        height: 100%;
    }

    .navbar-item:hover::after {
        content: "_";
        position: absolute;
        right: 0.5rem;
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
