<script>
    import NavbarLink from "./NavbarLink.svelte";
    import NavbarButton from "./NavbarButton.svelte";
    import { link } from "svelte-spa-router";
    import { navbarConfig } from "./config";
    import { startPage, accessLevel} from "../../../stores";
    import { accessLevels } from "../../types";
    import { onMount } from "svelte";
    import { blur } from "svelte/transition";

    let ready = false;
    let linkCount = 0;

    onMount(() => {
        ready = true;
    });
</script>

{#if ready}
    <nav class="navbar-container" in:blur={{ duration: 2000 }}>
        <a class="navbar-icon" href={$startPage} use:link>
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
        <div class="navbar-buttons">
            {#if $accessLevel >= accessLevels.user}
                {#each navbarConfig.authenticated.buttons as button}
                    <NavbarButton
                        label={button.label}
                        route={button.route}
                        variant={button.variant}
                    />
                {/each}
            {:else}
                {#each navbarConfig.default.buttons as button}
                    <NavbarButton
                        label={button.label}
                        route={button.route}
                        variant={button.variant}
                    />
                {/each}
            {/if}
        </div>
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

    .navbar-buttons {
        display: flex;
        align-items: center;
        padding-right: 2rem;
    }
</style>
