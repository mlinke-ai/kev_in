<script lang="ts">
  import { exerciseTypes } from "../../lib/constants";
  import { Exercise, getExercise } from "../../lib/Excercises/exercise";
  import CodeSandbox from "./CodeSandbox.svelte";
  import ParsonsPuzzleExercise from "./ParsonsPuzzleExercise.svelte";

  export let params: { exerciseID: number };
  let exerciseID = params.exerciseID;
  let exerciseData: Exercise;
  let ready = false;

  getExercise(exerciseID).then((data) => {
    exerciseData = data;
    ready = true;
  });
</script>

{#if ready}
  {#if exerciseData.exercise_type == exerciseTypes.programming}
    <CodeSandbox {exerciseData}/>
  {:else if exerciseData.exercise_type == exerciseTypes.parsonsPuzzle}
    <ParsonsPuzzleExercise />
  {/if}
{/if}
