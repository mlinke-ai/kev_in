<script>
    import NavbarItem from "./NavbarItem.svelte"
    import { navbarSettings } from "./config"
</script>

<nav class="navbar-container">
    <ul class="navbar-navigation">
        {#each navbarSettings.items as item}
            <NavbarItem label={item.label} route={item.route} icon={item.icon} />
        {/each}
    </ul>
</nav>

<style>
    .navbar-container {
        position: fixed;
        margin: 0;
        top: 0;
        left: 0;
        width: 100vw;
        height: 4rem;
        background-color: #005f50;
        display: flex;
    }
    .navbar-navigation {
        margin: auto;
        display: flex;
        align-items: center;
    }
</style>