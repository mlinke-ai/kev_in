export let navbarConfig = {
    logo: {
        src: "assets/logo_main.svg",
        alt: "Kev.In"
    },
    default: {
        links: [
            {
                label: "Lecture",
                route: "#/lecture",
            },
            {
                label: "Training",
                route: "#/training",
            },
            {
                label: "Coding",
                route: "#/coding",
            },
            //{
            //    label: "MyRoute",
            //    route: "#/my-route",
            //},
        ],
        buttons: [
            {
                label: "Register",
                route: "#/register",
                variant: "outlined"
            },
            {
                label: "Login",
                route: "#/login",
                variant: "unelevated"
            }
        ]
    },
    admin: {
        links: [
            {
                label: "Users",
                route: "#/users",
                icon: "",
            },
            {
                label: "Stats",
                route: "#/stats",
                icon: "",
            },
        ]
    }
    
}