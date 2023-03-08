<script lang="ts">
  import type { ExerciseGet } from "./types";
  import { getExercise } from "./exercise";
  import type { ComponentType } from "svelte";
  import Message from "../Common/Message/Message.svelte";
  import { messages } from "../Common/types";
  export let exerciseID: number;

  let exerciseData: ExerciseGet;
  let exerciseComponent: ComponentType;
  let exercisePromise = get();
  let errorMsg = Message

  async function get() {
    try {
      getExercise(exerciseID).then((data) => {
        exerciseData = data;
        import(`./${exerciseData.exercise_type_name}/${exerciseData.exercise_type_name}.svelte`).then((component) => exerciseComponent = component.default)
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
  <Message bind:message={errorMsg} content={error} type={messages.error} autoOpen={true}/>
{/await}
