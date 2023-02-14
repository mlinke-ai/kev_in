<script>
    import { getExercise } from "../../lib/Excercises/exercise";

    export let params = {};
    let exerciseID = params.exerciseID;

    console.log(getExercise(exerciseID));
</script>
