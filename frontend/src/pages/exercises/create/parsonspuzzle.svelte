<script>
  import Button from "@smui/button/src/Button.svelte";
  import Page from "../../../lib/Common/Page.svelte";
  import Textfield from "@smui/textfield";
  import IconButton from '@smui/icon-button';
  import ExitDialog from "../../../lib/Excercises/ExitDialog.svelte";
  import { Icon, Label } from "@smui/button";
  import TaskCardCreation from "../../../lib/Excercises/TaskCardCreation.svelte";

  let itemsLeft = [];
  $: itemsLeft = [{id: 1, name: ""}];

  let exerciseTitle = "";
  let exerciseDescription = "";

  let openExit = false;

  function newPuzzlePiece(){
    itemsLeft = [...itemsLeft, {id: itemsLeft.length + 1, name: ""}]
  }

  function deletePuzzlePiece(idx){
    idx --;
    itemsLeft.splice(idx, 1);
    for(let k = idx; k < itemsLeft.length; k++){
      itemsLeft[k]["id"] --;
    }
    itemsLeft = itemsLeft
  }

  function reset(){
    itemsLeft = [{id: 1, name: ""}];
    exerciseDescription = "";
    exerciseTitle = "";
  }


  const submitExercise = async () =>{
    fetch(
      "/exercise",
      {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          exercise_title: exerciseTitle,
          exercise_description: exerciseDescription,
          exercise_type: 3,
          exercise_content: {
            list: itemsLeft.map(item => item.name)
          },
          exercise_language: 1,
          exercise_solution: {
            list: itemsLeft.map(item => item.name)
          },
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
      <TaskCardCreation bind:description={exerciseDescription} />
    </div>
    <div class="creation-area">
      {#each itemsLeft as item(item.id)}
        <div style="display: flex; flex-direction: row; align-items: center">
          <Textfield textarea bind:value={item.name} label={"Puzzle Piece #" + item.id} style="width: 100%;"></Textfield>
          <IconButton class="material-icons" on:click={() => deletePuzzlePiece(item.id)}>delete</IconButton>
        </div>
      {/each}
      <Button variant="raised" on:click={newPuzzlePiece}>Add a new Puzzle Piece</Button>
    </div>
    <div class="status-bar">
      <Button variant ="outlined" on:click={()=>{openExit=true}}>
        <Icon class="material-icons">arrow_back</Icon>
        <Label>Back to Overview</Label>
      </Button>
      <div>
        <Button variant="outlined" on:click={reset}>
          <Icon class="material-icons">restart_alt</Icon>
          <Label>Reset</Label>
        </Button>
        <Button variant="raised" on:click={submitExercise}>Submit new Exercise</Button>
      </div>
    </div>
  </div>
  <ExitDialog bind:open={openExit}/>
</Page>

<style lang="scss">
  @use "../../../variables" as vars;

  .exercise-container {
    display: grid;
    grid-template-columns: 3fr 9fr;
    grid-template-rows: auto 9fr auto;
    grid-template-areas:
      "head head"
      "task creation-area"
      "status status";
    gap: 0.5rem;
    height: 98vh;
    padding: 0.5rem 0.5rem 0.5rem 0.5rem;
  }

  .header-area {
    grid-area: head;
    height: max-content;
  }
  .task-area {
    grid-area: task;
  }
  .creation-area {
    grid-area: creation-area;
    display: flex;
    flex-direction: column;
    overflow: auto;
    gap: 10px;
    padding-top: 5px;
  }
  .status-bar {
    grid-area: status;
    font-family: "Roboto Mono";
    display: flex;
    align-items: center;
    gap: auto;
    justify-content: space-between;
    height: max-content;
  }

</style>
