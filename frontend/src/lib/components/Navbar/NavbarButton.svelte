<script>
    // @ts-nocheck
    import Button from "@smui/button";
    import { onMount } from "svelte";

    export let label = "";
    export let route = "";
    export let variant = "outlined";
</script>

<div class="navbar-button">
    <a href={route}>
        <Button {variant}>{label}</Button>
    </a>
</div>

<style>
    .navbar-button {
        margin-left: 1rem;
    }
</style>
