<script>
  import Message from "../../lib/common/Message/Message.svelte";
  import { messages } from "../../lib/constants";
  import { getExercise } from "../../lib/Excercises/exercise";

  export let params = {};
  let exerciseID = params.exerciseID;
  let exerciseData;

  let error;
  let errorMessage;

  getExercise(exerciseID).then((data) => {
    if (data) {
      exerciseData = data[exerciseID];
    } else {
      error = "Error.";
      errorMessage.open();
    }
  });
</script>

<Message bind:errorMessage message={error} type={messages.error} />
