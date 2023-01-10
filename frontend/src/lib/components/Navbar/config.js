export let navbarConfig = {
    logo: {
        src: "assets/logo_main.svg",
        alt: "Kev.In"
    },
    default: {
        links: [
            //{
            //    label: "MyRoute",
            //    route: "/my-route",
            //},
        ],
        buttons: [
            {
                label: "Signup",
                route: "/signup",
                variant: "outlined"
            },
            {
                label: "Login",
                route: "/login",
                variant: "unelevated"
            }
        ]
    },
    authenticated: {
        links: [],
        buttons: []
    },
    admin: {
        links: [
            {
                label: "Users",
                route: "/users",
                icon: "",
            },
            {
                label: "Stats",
                route: "/stats",
                icon: "",
            },
        ]
    }
}