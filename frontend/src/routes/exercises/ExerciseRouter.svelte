<script lang="ts">
  import { exercises } from "../../lib/constants";
  import { Exercise, getExercise } from "../../lib/Excercises/exercise";
  import CodeSandbox from "./ProgrammingExercise.svelte";
  import ParsonsPuzzleExercise from "./ParsonsPuzzleExercise.svelte";

  export let params: { exerciseID: number };
  let exerciseID = params.exerciseID;
  let exerciseData: Exercise;
  let ready = false;

  getExercise(exerciseID).then((data) => {
    exerciseData = data;
    console.log(exerciseData)
    ready = true;
  });
</script>

{#if ready}
  {#if exerciseData.exercise_type == exercises.programming}
    <CodeSandbox {exerciseData}/>
  {:else if exerciseData.exercise_type == exercises.parsonsPuzzle}
    <ParsonsPuzzleExercise />
  {/if}
{/if}
