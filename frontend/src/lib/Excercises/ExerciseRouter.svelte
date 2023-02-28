<script lang="ts">
  import { exercises, ExerciseGet } from "./types";
  import { getExercise } from "./exercise";
  import ProgrammingExercise from "./Programming/Programming.svelte";
  import ParsonsPuzzleExercise from "../../lib/Excercises/ParsonsPuzzle/ParsonsPuzzleExercise.svelte";
  import type { ExerciseGetProgramming } from "./Programming/types";
  import type { ComponentType } from "svelte";

  export let exerciseID: number;

  let exerciseData: ExerciseGet;
  let exerciseComponent: ComponentType;
  let exercisePromise = get();

  async function get() {
    try {
      getExercise(exerciseID).then((data) => {
        exerciseData = data;
        switch (exerciseData.exercise_type_value) {
          case exercises.parsonsPuzzle:
            exerciseData = exerciseData;
            exerciseComponent = ParsonsPuzzleExercise;
            break;
          case exercises.programming:
            exerciseData = exerciseData as ExerciseGetProgramming;
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
