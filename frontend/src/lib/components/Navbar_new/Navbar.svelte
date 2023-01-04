<script>
</script>

<nav class="navbar-container">
    <ul class="navbar-nav">
        <li class="logo">
            <div class="nav-link">
                A
                <span class="link-text">Test</span>
            </div>
        </li>
        <li class="nav-item">
            <div class="nav-link">
                B
                <span class="link-text">Test</span>
            </div>
        </li>
    </ul>
</nav>

<style lang="scss">
    $navbar-contrast-color: orange;
    $navbar-bg-primary: #23232e;
    $navbar-bg-secondary: #141418;
    $navbar-bg-tertiary: black;
    $navbar-text-primary: #b6b6b6;
    $navbar-text-secondary: #ececec;
    $navbar-transition-speed: 200ms;

    .navbar-container {
        position: fixed;
        top: 0;
        left: 0;
        background-color: $navbar-bg-primary;
        transition: 200ms ease;
        z-index: 999;
        user-select: none;
        opacity: 0.95;
    }

    .navbar-nav {
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 100%;
        margin: 0;
        padding: 0;
        list-style: none;
    }

    .nav-item:nth-last-child(2) {
        margin-top: auto;
    }

    .nav-link {
        display: flex;
        align-items: center;
        height: 5rem;
        color: $navbar-text-primary;
        text-decoration: none;
        filter: grayscale(100%) opacity(0.7);
        transition: $navbar-transition-speed;
    }

    .nav-action {
        align-items: center;
        height: 5rem;
        color: $navbar-text-primary;
        text-decoration: none;
        filter: grayscale(100%) opacity(0.7);
        transition: $navbar-transition-speed;
        display: none;
        opacity: 0;
    }

    .nav-action:hover {
        filter: grayscale(0%) opacity(1);
        color: $navbar-text-secondary;
    }

    .nav-link:hover {
        filter: grayscale(0%) opacity(1);
        background: $navbar-bg-secondary;
        color: $navbar-text-secondary;
    }

    .nav-link:hover i {
        transform: translate(0px, -2px);
        /*transform: scale(1.05)*/
        transition: 300ms;
    }

    .link-text {
        display: none;
        opacity: 0;
        margin-left: 1.5rem;
        user-select: none;
    }

    @keyframes fade_in {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes delay_fade_in {
        from {
            opacity: 0;
        }
        to {
            opacity: 0;
        }
    }

    .nav-link i {
        color: $navbar-contrast-color;
        min-width: 2rem;
        max-width: 2rem;
        margin: 0 1.5rem;
    }

    .logo {
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 1rem;
        text-align: center;
        color: $navbar-text-secondary;
        background: $navbar-bg-tertiary;
        font-size: 1.2rem;
        letter-spacing: 0.3ch;
        width: 100%;
    }

    .logo i {
        transform: rotate(0deg);
        transition: transform $navbar-transition-speed;
    }

    .navbar-container:hover .logo i {
        transform: rotate(360deg);
    }

    .nav-item {
        width: 100%;
    }

    @media only screen and (max-width: 75rem) {
        main {
            padding-top: 6rem;
        }

        .navbar-container {
            height: 5rem;
            width: 100vw;
            overflow-x: scroll;
            overflow-y: hidden;
        }

        .navbar-container::-webkit-scrollbar {
            height: 0.1rem;
        }

        .navbar-container::-webkit-scrollbar-track {
            background: #1e1e24;
        }

        .navbar-container::-webkit-scrollbar-thumb {
            background: $navbar-contrast-color;
        }

        .logo {
            display: none;
        }

        .navbar-nav {
            flex-direction: row;
        }

        .nav-link {
            justify-content: center;
        }

        .nav-link:hover {
            border-bottom: 5px solid $navbar-contrast-color;
        }
    }

    @media only screen and (min-width: 75rem) {
        main {
            margin-left: 5rem;
            padding: 1rem;
        }

        .navbar-container {
            top: 0;
            width: 5rem;
            height: 100vh;
            overflow-x: hidden;
            overflow-y: auto;
        }

        .navbar-container:hover {
            width: 18rem;
        }

        .navbar-container:hover .link-text {
            display: block;
            animation: fade_in $navbar-transition-speed;
            opacity: 1;
        }

        .navbar-container:hover .nav-action {
            display: flex;
            animation: fade_in 2 * $navbar-transition-speed;
            opacity: 1;
        }

        .nav-link:hover {
            border-right: 5px solid $navbar-contrast-color;
        }

        .nav-item:last-child {
            margin-bottom: 1rem;
        }
    }
</style>
