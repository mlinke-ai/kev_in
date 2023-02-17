<script lang="ts">
  import { exercises, messages } from "../../lib/constants";
  import { ProgrammingExerciseType, getExercise, ParsonsPuzzleExerciseType } from "../../lib/Excercises/exercise";
  import ProgrammingExercise from "./ProgrammingExercise.svelte";
  import ParsonsPuzzleExercise from "./ParsonsPuzzleExercise.svelte";
  import Message from "../../lib/common/Message/Message.svelte";
  export let params: { exerciseID: number };
  let exerciseID = params.exerciseID;
  let exerciseData: ProgrammingExerciseType | ParsonsPuzzleExerciseType;
  let messageComponent;
  let ready = false;

  let parsonsPuzzleData: ParsonsPuzzleExerciseType;
  let programmingData: ProgrammingExerciseType;

  getExercise(exerciseID).then((data) => {
    exerciseData = data;
    switch (exerciseData.exercise_type_name) {
      case exercises.parsonsPuzzle:
        parsonsPuzzleData = exerciseData as ParsonsPuzzleExerciseType;
        break
      case exercises.programming:
      programmingData = exerciseData as ProgrammingExerciseType;
        break
    }
    ready = true;
  });
</script>

{#if ready}
  {#if exerciseData.exercise_type_name == exercises.programming}
    <ProgrammingExercise exerciseData={programmingData} />
  {:else if exerciseData.exercise_type_name == exercises.parsonsPuzzle}
    <ParsonsPuzzleExercise exerciseData={parsonsPuzzleData}/>
  {:else}
    <Message
      bind:message={messageComponent}
      content={`A component for exercise type "${exerciseData.exercise_type_name}" does not
      exist yet.`}
      type={messages.error}
      autoOpen={true}
    />
  {/if}
{/if}
