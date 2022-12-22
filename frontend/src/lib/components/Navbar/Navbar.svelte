<script>
    import NavbarLink from "./NavbarLink.svelte";
    import NavbarButton from "./NavbarButton.svelte";
    import { navbarConfig } from "./config";
    import { userLoggedIn, userIsAdmin } from "../../../stores";
    import { onMount } from "svelte";
    import { blur } from "svelte/transition";

    let ready = false
    let linkCount = 0

onMount(() => {
    ready = true
})
</script>

{#if ready}
<nav class="navbar-container" in:blur="{{ duration: 2000 }}">
    <a class="navbar-icon" href="/#">
        <img src={navbarConfig.logo.src} alt={navbarConfig.logo.alt} />
    </a>
    <ul class="navbar-links">
        {#if $userIsAdmin}
            {#each navbarConfig.admin.links as item, index}
                <NavbarLink label={item.label} route={item.route} id={index} />
            {/each}
        {/if}
        {#each navbarConfig.default.links as item, index}
            <NavbarLink label={item.label} route={item.route} id={linkCount + index} />
        {/each}
    </ul>
    <div class="navbar-buttons">
        {#if $userLoggedIn}
            <NavbarButton
                label="Profile"
                route="#/profile"
                variant="unelevated"
            />
        {:else}
            {#each navbarConfig.default.buttons as button, index}
                    <NavbarButton
                        label={button.label}
                        route={button.route}
                        variant={button.variant}
                        id={navbarConfig.default.links.length + index}
                    />
            {/each}
        {/if}
    </div>
</nav>
{/if}

<style>
    .navbar-container {
        position: fixed;
        margin: auto;
        box-sizing:border-box;
        top: 0;
        left: 0;
        width: 100vw;
        display: flex;
        align-items: center;
        background-color: none;
        font-family: "Roboto";
        z-index: 999;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .navbar-icon {
        display: flex;
        align-items: center;
        width: 10rem;
        margin: 1rem;
        font-family: "Roboto Mono";
    }

    .navbar-links {
        display: flex;
        align-items: center;
        margin-left: auto;
        padding-right: 2rem;
    }

    .navbar-buttons {
        display: flex;
        align-items: center;
        padding-right: 2rem;
    }
</style>
