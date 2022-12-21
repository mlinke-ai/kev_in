<script>
    import NavbarLink from "./NavbarLink.svelte"
    import NavbarButton from "./NavbarButton.svelte"
    import { navbarConfig } from "./config"
    import Logo from "../Logo/Logo.svelte"

    let loggedIn = false
    let admin = false
</script>

<nav class="navbar-container">

    <a href="/#">
        <div class="navbar-icon">
            <Logo/>
        </div>
    </a>

    <ul class="navbar-links">
        {#if admin}
            {#each navbarConfig.admin.items as item}
                <NavbarLink label={item.label} route={item.route} icon={item.icon} />
            {/each}
        {/if}
        {#each navbarConfig.default.items as item}
            <NavbarLink label={item.label} route={item.route} icon={item.icon} />
        {/each}
    </ul>
    <div class="navbar-buttons">
        {#if loggedIn}
            <NavbarButton label="Profile" route="#/profile" variant="unelevated" />
        {:else}
            <NavbarButton label="Register" route="#/register" variant="outlined" />
            <NavbarButton label="Login" route="#/auth" variant="unelevated" />
        {/if}
    </div>
</nav>

<style>
    .navbar-container {
        position: fixed;
        margin: 0;
        top: 0;
        left: 0;
        width: 100vw;
        height: 4rem;
        display: flex;
        background-color: #333333;
        font-family: "Roboto";
        z-index: 999;
    }

    .navbar-icon {
        /* display: flex; */
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-family: "Roboto Mono";
        width: 10rem;
        position: relative;
        margin: auto;
        top: 20%
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