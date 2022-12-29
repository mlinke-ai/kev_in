<!-- Skeletton component for all pages to provide 
    unified transitions and title naming -->

<script>
    import { blur } from "svelte/transition";

    export let transition = true;
    export let title = "";
</script>

<svelte:head>
    {#if title}
        <title>Kev.In - {title}</title>
    {:else}
        <title>Kev.In</title>
    {/if}
</svelte:head>

{#if transition}
    <div class="page" in:blur="{{ duration: 250 }}">
        <slot />
    </div>
{:else}
    <div class="page">
        <slot />
    </div>
{/if}
