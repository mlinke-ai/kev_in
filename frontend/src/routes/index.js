import Home from "./Home.svelte"
import Dashboard from "./Dashboard.svelte"
import Error from "./Error.svelte"
import CodeSandbox from "./CodeSandbox.svelte"
import BlanksExercise from "./BlanksExercise.svelte"
import AdminDashboard from "./AdminDashboard.svelte"
import Exercises from "./Exercises.svelte"
import Users from "./Users.svelte"
import AddUser from "./AddUser.svelte"
import ParsonsPuzzleExercise from "./ParsonsPuzzleExercise.svelte"
import ParsonsPuzzleExerciseCreate from "./ParsonsPuzzleExerciseCreate.svelte"
//import ExamplePage from "./Example.svelte"

export default {
    "/": Home,
    "/dashboard": Dashboard,
    "/parsonspuzzle": ParsonsPuzzleExercise,
    "/ppecreation": ParsonsPuzzleExerciseCreate,
    "/sandbox": CodeSandbox,
    "/blanks": BlanksExercise,
    "/admin-dashboard": AdminDashboard,
    "/exercises": Exercises,
    "/users": Users,
    "/adduser": AddUser,
    //"/example-path": <ExamplePage>,
    "*": Error
}