<script lang="ts">
  import {
    exercises,
    ProgrammingExerciseType,
    ParsonsPuzzleExerciseType,
  } from "../../lib/Excercises/types";
  import { getExercise } from "../../lib/Excercises/exercise";
  import ProgrammingExercise from "./ProgrammingExercise.svelte";
  import ParsonsPuzzleExercise from "./ParsonsPuzzleExercise.svelte";

  export let params: { exerciseID: number };
  let exerciseID = params.exerciseID;

  let exerciseData: ProgrammingExerciseType | ParsonsPuzzleExerciseType;
  let exerciseComponent;
  let exercisePromise = get();

  async function get() {
    try {
      exerciseData = await getExercise(exerciseID);
      switch (exerciseData.exercise_type_name) {
        case exercises.parsonsPuzzle:
          exerciseComponent = ParsonsPuzzleExercise;
          break;
        case exercises.programming:
          exerciseComponent = ProgrammingExercise;
          break;
      }
    } catch (err) {
      console.error(err);
      throw err;
    }
  }
</script>

{#await exercisePromise}
  Loading exercise...
{:then _}
  <svelte:component this={exerciseComponent} {exerciseData} />
{:catch error}
  <!-- TODO: Error Handling -->
  {error}
{/await}
