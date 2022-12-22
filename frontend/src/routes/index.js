import Home from "./Home.svelte"
import Login from "./Login.svelte"
import Profile from "./Profile.svelte"
import Error from "./Error.svelte"

export default {
    "/": Home,
    "/login": Login,
    "/profile": Profile,
    // new pages here -> "/<path>": <PageName>,
    "*": Error
}