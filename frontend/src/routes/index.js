import Home from "./HomeTest.svelte"
import Login from "./Login.svelte"
import Profile from "./Profile.svelte"
import Error from "./Error.svelte"
import CodeSandbox from "./CodeSandbox.svelte"
//import ExamplePage from "./Example.svelte"

export default {
    "/": Home,
    "/login": Login,
    "/profile": Profile,
    "/sandbox": CodeSandbox,
    //"/example-path": <ExamplePage>,
    "*": Error
}