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