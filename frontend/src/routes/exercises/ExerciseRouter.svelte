<!-- Component for routing to a specific exercise -->

<script lang="ts">
  import { exercises, messages } from "../../lib/constants";
  import { ProgrammingExerciseType, getExercise, ParsonsPuzzleExerciseType } from "../../lib/Excercises/exercise";
  import ProgrammingExercise from "./ProgrammingExercise.svelte";
  import ParsonsPuzzleExercise from "./ParsonsPuzzleExercise.svelte";
  import Message from "../../lib/common/Message/Message.svelte";
  
  // variable to get the exerciseID from the url
  export let params: { exerciseID: number };

  let exerciseID = params.exerciseID;
  let exerciseData: ProgrammingExerciseType | ParsonsPuzzleExerciseType;
  let messageComponent: Message;
  let ready = false;

  let parsonsPuzzleData: ParsonsPuzzleExerciseType;
  let programmingData: ProgrammingExerciseType;

  // fetch detailed exercise info from the server
  getExercise(exerciseID).then((data) => {
    exerciseData = data;
    // decide which data type to choose based on exercise_type
    switch (exerciseData.exercise_type) {
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

<!-- render the selected exercise page -->
{#if ready}
  {#if exerciseData.exercise_type == exercises.programming}
    <ProgrammingExercise exerciseData={programmingData} />
  {:else if exerciseData.exercise_type == exercises.parsonsPuzzle}
    <ParsonsPuzzleExercise exerciseData={parsonsPuzzleData}/>
  {:else}
    <Message
      bind:message={messageComponent}
      content={`A component for exercise type "${exerciseData.exercise_type}" does not
      exist yet.`}
      type={messages.error}
      autoOpen={true}
    />
  {/if}
{/if}
