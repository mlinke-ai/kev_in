import Home from "./Home.svelte"
import Dashboard from "./Dashboard.svelte"
import Error from "./Error.svelte"
import CodeSandbox from "./CodeSandbox.svelte"
import ParsonsPuzzleExercise from "./ParsonsPuzzleExercise.svelte"
//import ExamplePage from "./Example.svelte"

export default {
    "/": Home,
    "/dashboard": Dashboard,
    "/parsonspuzzle": ParsonsPuzzleExercise,
    "/sandbox": CodeSandbox,
    //"/example-path": <ExamplePage>,
    "*": Error
}