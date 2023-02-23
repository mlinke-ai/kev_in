import Home from "./Home.svelte"
import Dashboard from "./Dashboard.svelte"
import Error from "./Error.svelte"
import CodeSandbox from "./exercises/ProgrammingExercise.svelte"
import AdminDashboard from "./AdminDashboard.svelte"
import UserDashboard from "./UserDashboard.svelte"
import Solutions from "./Solutions.svelte"
import Exercises from "./exercises/Exercises.svelte"
import Users from "./Users.svelte"
import AddUser from "./AddUser.svelte"
import ParsonsPuzzleExercise from "./exercises/ParsonsPuzzleExercise.svelte"
import ParsonsPuzzleExerciseCreate from "./exercises/create/ParsonsPuzzleExerciseCreate.svelte"
import ExerciseRouter from "./exercises/ExerciseRouter.svelte"
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
    "/exercises/:exerciseID": ExerciseRouter,
    "/users": Users,
    "/adduser": AddUser,
    //"/example-path": <ExamplePage>,
    "*": Error
}