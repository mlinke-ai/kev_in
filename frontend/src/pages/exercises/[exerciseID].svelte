<script lang="ts">
  import {
    exercises,
    ProgrammingExerciseType,
    ParsonsPuzzleExerciseType,
  } from "../../lib/Excercises/types";
  import { getExercise } from "../../lib/Excercises/exercise";
  import ProgrammingExercise from "../../lib/Excercises/Programming/ProgrammingExercise.svelte";
  import ParsonsPuzzleExercise from "../../lib/Excercises/ParsonsPuzzle/ParsonsPuzzleExercise.svelte";

  export let exerciseID: any;
  exerciseID = exerciseID as unknown as number;

  let exerciseData: ProgrammingExerciseType | ParsonsPuzzleExerciseType;
  let exerciseComponent;
  let exercisePromise = get();

  async function get() {
    try {
      getExercise(exerciseID).then((data) => {
        exerciseData = data;
        switch (exerciseData.exercise_type_value) {
          case exercises.parsonsPuzzle:
            exerciseComponent = ParsonsPuzzleExercise;
            break;
          case exercises.programming:
            exerciseComponent = ProgrammingExercise;
            break;
        }
      });
    } catch (err) {
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
