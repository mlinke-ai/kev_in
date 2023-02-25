<script lang="ts">
  import { exercises } from "../../../lib/Excercises/types";
  import ParsonsPuzzle from "./parsonspuzzle.svelte";
  import Programming from "./programming.svelte";

  export let exerciseID: any;
  exerciseID = exerciseID as unknown as number;
  let exerciseComponent;

  console.log(exerciseID, exercises.parsonsPuzzle)

  switch (exerciseID) {
    case <number>exercises.parsonsPuzzle:
      exerciseComponent = ParsonsPuzzle
    case <number>exercises.programming:
    exerciseComponent = Programming
  }
</script>

<svelte:component this={exerciseComponent} />