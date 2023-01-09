import Home from "./Home.svelte"
import Login from "./Login.svelte"
import Profile from "./Profile.svelte"
import Error from "./Error.svelte"
import CodeSandbox from "./CodeSandbox.svelte"
import SignUp from "./SignUp.svelte"
import ParsonsPuzzleExercise from "./ParsonsPuzzleExercise.svelte"
//import ExamplePage from "./Example.svelte"

export default {
    "/": Home,
    "/login": Login,
    "/signup": SignUp,
    "/profile": Profile,
    "/parsonspuzzle": ParsonsPuzzleExercise,
    "/sandbox": CodeSandbox,
    //"/example-path": <ExamplePage>,
    "*": Error
}