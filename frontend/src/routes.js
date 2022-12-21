import Home from "./routes/Home.svelte"
import Login from "./routes/Login.svelte"
import Error from "./routes/Error.svelte"

export default {
    "/": Home,
    "/auth": Login,
    "*": Error
}