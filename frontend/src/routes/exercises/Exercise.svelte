<script>
  import { exerciseTypes } from "../../lib/constants";
  import { getExercise } from "../../lib/Excercises/exercise";
  import CodeSandbox from "./CodeSandbox.svelte";
  import ParsonsPuzzleExercise from "./ParsonsPuzzleExercise.svelte";

  export let params = {};
  let exerciseID = params.exerciseID;
  let exerciseData;
  let ready = false;

  getExercise(exerciseID).then((data) => {
    if (data) {
      exerciseData = data[exerciseID];
      console.log(exerciseData.exercise_type);
      ready = true;
    }
  });
</script>

{#if ready}
  {#if exerciseData.exercise_type == exerciseTypes.programming}
    <CodeSandbox />
  {:else if exerciseData.exercise_type == exerciseTypes.parsonsPuzzle}
    <ParsonsPuzzleExercise />
  {/if}
{/if}