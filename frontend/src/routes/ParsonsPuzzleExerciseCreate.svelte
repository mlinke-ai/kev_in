<script>
  import Button from "@smui/button/src/Button.svelte";
  import Page from "../lib/components/common/Page.svelte";
  import Textfield from "@smui/textfield";

  import TestCard from "../lib/components/CodeSandbox/TestCard.svelte";
  import { each } from "svelte/internal";

  let itemsLeft = [];
  $: itemsLeft = [{id: 1, name: ""}];
  let itemsLeftOriginal = [];
  let itemsRight = [];

  let valueA = "";
  let exerciseTitle = "";

  function newPuzzlePiece(){
    itemsLeft = [...itemsLeft, {id: itemsLeft.length + 1, name: ""}]
  }


  const submitExercise = async () =>{
    fetch(
      "/exercise",
      {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          exercise_title: "Test",
          exercise_description: "My PPE Description",
          exercise_type: 3,
          exercise_content: "Content String",
        })
      }
    ).then(response => {
      if (response.status === 400){
        alert("A required argument was not sent!");
      }
      else if (response.status === 401){
        // redirect to login
        window.location.replace("/#/login");
      } else if (response.status === 403){
        alert("you naughty naughty")
      } else if (response.status === 409){
        alert("The exercise with the title " + " already exists!")
      } else if (response.status === 201){
        alert("Successfully submitted Exercise")
        response.json().then(data => {
          console.log(data);
        })
      }
    })
  }

</script>

<Page title="Create PPE" fullwidth={true}>
  <div class="exercise-container">
    <div class="header-area">
      <Textfield variant="filled" bind:value={exerciseTitle} label="Exercise Title" required style="width: 100%"/>
    </div>
    <div class="task-area">
      <TestCard />
    </div>
    <div class="creation-area">
      {#each itemsLeft as item(item.id)}
        <Textfield textarea bind:value={item.name} label={"Puzzle Piece #" + item.id}>
        </Textfield>
      {/each}
      <Button variant="raised" on:click={newPuzzlePiece}>Add a new Puzzle Piece</Button>
    </div>
    <div class="status-bar">
      PPE - Creation
      <div>
        <Button variant="outlined">Reset</Button>
        <Button variant="raised" on:click={submitExercise}>Submit new Exercise</Button>
      </div>
    </div>
  </div>
</Page>

<style lang="scss">
  @use "../variables" as vars;

  .exercise-container {
    display: grid;
    grid-template-columns: 3fr 9fr;
    grid-template-rows: 1.5fr 8fr 0.5fr;
    grid-template-areas:
      "head head"
      "task creation-area"
      "status status";
    gap: 1%;
    padding: 1rem 1rem 0.5rem 1rem;
    // background-color: rgb(0, 0, 0);
    // margin-left: 3%;
    height: 100%;
  }

  .header-area {
    grid-area: head;
  }
  .task-area {
    grid-area: task;
    overflow: auto;
  }
  .creation-area {
    grid-area: creation-area;
    display: flex;
    flex-direction: column;
    overflow: auto;
    gap: 10px;
    padding-top: 10px;
  }
  .status-bar {
    grid-area: status;
    color: vars.$consoleColor;
    font-family: "Roboto Mono";
    display: flex;
    align-items: center;
    gap: auto;
    justify-content: space-between;
  }

</style>
