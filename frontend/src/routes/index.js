import Home from "./Home.svelte"
import Profile from "./Profile.svelte"
import Error from "./Error.svelte"
import CodeSandbox from "./CodeSandbox.svelte"
import EditExercise from "./EditExercise.svelte"
//import ExamplePage from "./Example.svelte"

export default {
    "/": Home,
    "/profile": Profile,
    "/sandbox": CodeSandbox,
    "/edit-exercise": EditExercise,
    //"/example-path": <ExamplePage>,
    "*": Error
}