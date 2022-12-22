<script>
    // @ts-nocheck
    import Button from "@smui/button";
    import { onMount } from "svelte";
  import { blur } from "svelte/transition";

    export let label = "";
    export let route = "";
    export let variant = "outlined";
    export let id = 0;
    let ready = false

    onMount(() => {
        ready = true
    })
</script>

{#if ready}
<div class="navbar-button" in:blur="{{ duration: 250, delay: id * 250 }}">
    <a href={route}>
        <Button {variant}>{label}</Button>
    </a>
</div>
{/if}

<style>
    .navbar-button {
        margin-left: 1rem;
    }
</style>
