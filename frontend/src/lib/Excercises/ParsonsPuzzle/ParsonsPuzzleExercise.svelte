<script lang="ts">
  import Page from "../../Common/Page.svelte";
  import PuzzleCard from "./PuzzleCard.svelte";
  import TaskCard from "../TaskCard.svelte";
  import StatusBar from "../StatusBar.svelte";
  import { accessLevels } from "../../Common/types";
  import {
    SolutionPostParsonsPuzzle,
    submitSolution,
    getCurrentTimestamp
  } from "../solution";
  import type { ParsonsPuzzleExerciseType } from "../types";
  import Message from "../../Common/Message/Message.svelte";
  import { messages } from "../../Common/types";
  import Dialog, { Title, Content, Actions } from '@smui/dialog';
  import Button, { Label, Icon } from '@smui/button';
  import { startPage } from "../../../stores";

  export let exerciseData: ParsonsPuzzleExerciseType;

  let solution: SolutionPostParsonsPuzzle;

  let errorMessage;
  let openCorrectDialog = false;

  let itemsLeft = [];
  let itemsLeftOriginal = [];
  let itemsRight = [];
  let elapsedTime = 0;

  itemsRight = [];
  
  console.log(exerciseData)
  let exerciseContent = exerciseData.exercise_content.list;
  
  for (let i = 0; i < exerciseContent.length; i++) {
    itemsLeft[i] = { id: i + 1, name: exerciseContent[i] };
  }
  itemsLeftOriginal = itemsLeft.slice();

  function submit() {
    solution = {
      solution_exercise: exerciseData.exercise_id,
      solution_date: getCurrentTimestamp(),
      solution_duration: elapsedTime,
      solution_content: {
        list: itemsRight.map(item => item.name)
      }
    }
    try{
      submitSolution(solution).then((data) =>{
        console.log(data)
        if (data.solution_correct){
          openCorrectDialog = true;
          console.log("Congratulations!")
        }
        else{
          errorMessage.open()
        }
      });
    }
    catch (err) {
      alert(err.toString())
    }
  }

  function reset() {
    itemsLeft = itemsLeftOriginal.slice();
    itemsRight = [];
  }
</script>

<Page
  title="Parsons Puzzle Exercise"
  fullwidth={true}
>
  <div class="exercise-container">
    <div class="header-area">
      <h3>{exerciseData.exercise_title}</h3>
    </div>
    <div class="task-area">
      <TaskCard markdownSourceCode={exerciseData.exercise_description}/>
    </div>
    <div class="puzzle-area">
      <PuzzleCard bind:itemsLeft bind:itemsRight />
    </div>
    <StatusBar {reset} {submit} bind:elapsedTime />
  </div>
  <Message
  bind:message={errorMessage}
  content={"Wrong Answer, please try again..."}
  type={messages.error}
  />
  <Dialog
  bind:open = {openCorrectDialog}
  scrimClickAction=""
  escapeKeyAction=""
  aria-labelledby="mandatory-title"
  aria-describedby="mandatory-content"
>
  <Title id="mandatory-title">Congratulations!</Title>
  <Content id="mandatory-content">
    You solved that task correctly!
  </Content>
  <Actions>
    <Button variant ="outlined" on:click={()=>{history.pushState({}, null, `#${$startPage}`)}}>
      <Icon class="material-icons">arrow_back</Icon>
      <Label>Return to Overview</Label>
    </Button>
  </Actions>
</Dialog>
</Page>

<style lang="scss">
  @use "../../../variables" as vars;

  .exercise-container {
    display: grid;
    grid-template-columns: 3fr 9fr;
    grid-template-rows: 1.5fr 8fr 0.5fr;
    grid-template-areas:
      "head head"
      "task puzzle"
      "status status";
    gap: 1%;
    padding: 1rem 1rem 0.5rem 1rem;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background-color: black;
  }

  .header-area {
    grid-area: head;
    h3 {
      color: vars.$primaryDark;
    }
  }
  .task-area {
    grid-area: task;
    overflow: auto;
  }
  .puzzle-area {
    grid-area: puzzle;
    display: flex;
    overflow: hidden;
  }
</style>
