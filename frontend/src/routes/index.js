import Home from "./Home.svelte"
import Dashboard from "./Dashboard.svelte"
import Error from "./Error.svelte"
import CodeSandbox from "./CodeSandbox.svelte"
import ParsonsPuzzleExercise from "./ParsonsPuzzleExercise.svelte"
import ParsonsPuzzleExerciseCreate from "./ParsonsPuzzleExerciseCreate.svelte"
//import ExamplePage from "./Example.svelte"

export default {
    "/": Home,
    "/dashboard": Dashboard,
    "/parsonspuzzle": ParsonsPuzzleExercise,
    "/ppecreation": ParsonsPuzzleExerciseCreate,
    "/sandbox": CodeSandbox,
    //"/example-path": <ExamplePage>,
    "*": Error
}