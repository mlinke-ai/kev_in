<script lang="ts">
  import ExerciseRouter from "../../lib/Excercises/ExerciseRouter.svelte";

  export let exerciseID: any;
  exerciseID = exerciseID as unknown as number;

</script>

<ExerciseRouter {exerciseID}/>
