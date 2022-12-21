import Home from "./Home.svelte"
import Login from "./Login.svelte"
import Error from "./Error.svelte"

export default {
    "/": Home,
    "/login": Login,
    "*": Error
}