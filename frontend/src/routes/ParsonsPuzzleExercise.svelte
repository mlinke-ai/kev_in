<script>
  import {flip} from "svelte/animate";
  import {dndzone} from "svelte-dnd-action";
  import Button from "@smui/button/src/Button.svelte";
  import Page from "../lib/components/common/Page.svelte";
  import { Icon } from "@smui/common";
  import PuzzleCard from "../lib/components/ParsonsPuzzleExercise/PuzzleCard.svelte";

  import TestCard from "../lib/components/CodeSandbox/TestCard.svelte";

  let itemsLeft = [];
  let itemsLeftOriginal = [];
  let itemsRight = [];


  const getExercise = async () =>{
    fetch(
      "/exercise?exercise_id=1&exercise_limit=19", 
      {
        method: "GET",
        headers: {"Content-Type": "application/json"},
      }
    ).then((response) =>{
      if (response.status === 401){
        // REDIRECT to LOGIN
        console.log("No cookies")
      } else if (response.status === 403){
        console.log("No admin rights")
      } else if (response.status === 400){
        console.log("user_limit out of range")
      } else if (response.status === 200){
        itemsLeft = [
          {id: 1, name: "print(32 + 66 + sum([1,2,3]))"},
          {id: 2, name: "print(22)\n34"},
          {id: 3, name: "item3"},
          {id: 4, name: "item3"},
          {id: 5, name: "item3"},
          {id: 6, name: "item3"},
          {id: 7, name: "item3"},
          {id: 8, name: "item3"},
          {id: 9, name: "item4"}
        ];
        itemsLeftOriginal = itemsLeft.slice();
      }
    })
  }


  function reset(){
    itemsLeft = itemsLeftOriginal.slice();
    itemsRight = [];
  }

  let startTime = 0;
  let elapsedTime = 0;
  let intervallID;
  const startTimer = () => {
    startTime = Date.now();
    intervallID = setInterval(() => {
      const endTime = Date.now();
      elapsedTime = endTime - startTime;
    })
  }

  const resetTimer = () => {
    elapsedTime = 0;
    clearInterval(intervallID);
  }
  
  let maxTimeReached = false;
  const format = (min, sec) => {
    // format to 2 digits and if maximum of 59 minutes and 59 seconds is reached, stop it
    if (maxTimeReached || min >= 59 && sec >= 59){
      maxTimeReached = true;
      return "59:59";
    }
    else {
      return ("00"+min.toString()).slice(-2) + ":" + ("00"+sec.toString()).slice(-2);
    }
  }
  $: seconds = (Math.floor(elapsedTime / 1000) % 60);
  $: minutes = (Math.floor(elapsedTime / 1000 / 60) % 60);
  $: formattedTime = format(minutes, seconds);
  startTimer()
  
</script>

<Page title="Parsons Puzzle Exercise" fullwidth={true}>
  <div class="exercise-container">
    <div class="header-area">
      <h3>Parsons Puzzle Exercise</h3>
    </div>
    <div class="task-area">
      <TestCard />
    </div>
    <div class="puzzle-area">
      <PuzzleCard bind:itemsLeft bind:itemsRight />
    </div>
    <div class="status-bar">
      Getting Started - Attempt 1
      <div>
        <Button variant="outlined" on:click={reset}>Reset</Button>
        <Button variant="raised" on:click={getExercise}>Submit</Button>
      </div>
      <div class="clock-widget">
        {formattedTime}
        <Icon class="material-icons">access_time</Icon>
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
    // margin-left: 3%;
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
  .status-bar {
    grid-area: status;
    color: vars.$consoleColor;
    font-family: "Roboto Mono";
    display: flex;
    align-items: center;
    gap: auto;
    justify-content: space-between;
  }
  .clock-widget {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
</style>
