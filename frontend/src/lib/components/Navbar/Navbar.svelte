<script>
    import NavbarLink from "./NavbarLink.svelte";
    import { link } from "svelte-spa-router";
    import { navbarConfig } from "./config";
    import { accessLevel } from "../../../stores";
    import { accessLevels } from "../../constants";
    import { onMount } from "svelte";
    import { blur } from "svelte/transition";
    import IconButton from "@smui/icon-button";
    import AccountMenu from "./AccountMenu.svelte";

    let ready = false;
    let linkCount = 0;

    onMount(() => {
        ready = true;
    });
</script>

{#if ready}
    <nav class="navbar-container" in:blur={{ duration: 2000 }}>
        <a class="navbar-icon" href={"/"} use:link>
            <img src={navbarConfig.logo.src} alt={navbarConfig.logo.alt} />
        </a>
        <ul class="navbar-links">
            {#each navbarConfig.default.links as item, index}
                <NavbarLink
                    label={item.label}
                    route={item.route}
                    id={linkCount + index}
                />
            {/each}
            {#if $accessLevel == accessLevels.admin}
                {#each navbarConfig.admin.links as item, index}
                    <NavbarLink
                        label={item.label}
                        route={item.route}
                        id={index}
                    />
                {/each}
            {:else if $accessLevel >= accessLevels.user}
                {#each navbarConfig.authenticated.links as item, index}
                    <NavbarLink
                        label={item.label}
                        route={item.route}
                        id={linkCount + index}
                    />
                {/each}
            {/if}
        </ul>
        {#if $accessLevel > 0}
            <AccountMenu />
        {/if}
    </nav>
{/if}

<style lang="scss">
    .navbar-container {
        position: fixed;
        margin: auto;
        box-sizing: border-box;
        top: 0;
        left: 0;
        width: 100vw;
        display: flex;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.2);
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
</style>
