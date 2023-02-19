<script lang="ts">
  import { exercises } from "../../lib/constants";
  import {
    ProgrammingExerciseType,
    getExercise,
    ParsonsPuzzleExerciseType,
  } from "../../lib/Excercises/exercise";
  import ProgrammingExercise from "./ProgrammingExercise.svelte";
  import ParsonsPuzzleExercise from "./ParsonsPuzzleExercise.svelte";
  import Error from "../Error.svelte";

  export let params: { exerciseID: number };
  let exerciseID = params.exerciseID;

  let exerciseData: ProgrammingExerciseType | ParsonsPuzzleExerciseType;
  let exerciseComponent;
  let exercisePromise = get();

  async function get() {
    getExercise(exerciseID).then((data) => {
      exerciseData = data;
      switch (exerciseData.exercise_type_name) {
        case exercises.parsonsPuzzle:
          exerciseComponent = ParsonsPuzzleExercise;
          break;
        case exercises.programming:
          exerciseComponent = ProgrammingExercise;
          break;
      }
    });
  }
</script>

{#await exercisePromise}
  Loading exercise...
{:then _}
  <svelte:component this={exerciseComponent} {exerciseData} />
{:catch error}
  <!-- TODO: Error Handling -->
{/await}
