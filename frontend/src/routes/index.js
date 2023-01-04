import Home from "./HomeTest.svelte"
import Login from "./Login.svelte"
import Profile from "./Profile.svelte"
import Error from "./Error.svelte"
//import ExamplePage from "./Example.svelte"

export default {
    "/": Home,
    "/login": Login,
    "/profile": Profile,
    //"/example-path": <ExamplePage>,
    "*": Error
}