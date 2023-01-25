import Home from "./Home.svelte"
import Login from "./Login.svelte"
import Profile from "./Profile.svelte"
import Error from "./Error.svelte"
import CodeSandbox from "./CodeSandbox.svelte"
import SignUp from "./SignUp.svelte"
import AdminDashboard from "./AdminDashboard.svelte"
import Exercises from "./Exercises.svelte"
import Users from "./Users.svelte"
//import ExamplePage from "./Example.svelte"

export default {
    "/": Home,
    "/login": Login,
    "/signup": SignUp,
    "/profile": Profile,
    "/sandbox": CodeSandbox,
    "/admin-dashboard": AdminDashboard,
    "/exercises": Exercises,
    "/users": Users,
    //"/example-path": <ExamplePage>,
    "*": Error
}