import Home from "./Home.svelte"
import Dashboard from "./Dashboard.svelte"
import Error from "./Error.svelte"
import CodeSandbox from "./CodeSandbox.svelte"
import AdminDashboard from "./AdminDashboard.svelte"
import UserDashboard from "./UserDashboard.svelte"
import Exercises from "./Exercises.svelte"
import Solutions from "./Solutions.svelte"
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
    "/admin-dashboard": AdminDashboard,
    "/user-dashboard": UserDashboard,
    "/exercises": Exercises,
    "/solutions": Solutions,
    "/users": Users,
    "/adduser": AddUser,
    //"/example-path": <ExamplePage>,
    "*": Error
}