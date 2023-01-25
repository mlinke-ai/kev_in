<script>
  import {flip} from "svelte/animate";
  import {dndzone} from "svelte-dnd-action";
  import Page from "../lib/components/common/Page.svelte";
  import PuzzleCard from "../lib/components/Excercises/ParsonsPuzzle/PuzzleCard.svelte";
  import { userName } from "../stores";

  import TestCard from "../lib/components/CodeSandbox/TestCard.svelte";
  import StatusBar from "../lib/components/Excercises/StatusBar.svelte";
  import { accessLevels } from "../lib/types";

  let itemsLeft = [];
  let itemsLeftOriginal = [];
  let itemsRight = [];
  let exerciseID = null;
  let exerciseTitle = "Exercise";
  let exerciseDescription = "Please use your Brain"
  let exerciseContent = ""


  function getCurrentTimestamp () {
    return Date.now()
  }

  const submitSolution = async (exercise_id) =>{
    fetch(
      "/solution?solution_exercise=" + exercise_id,
      {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          solution_user: 1,
          solution_exercise: exerciseID,
          solution_date: getCurrentTimestamp(),
          solution_duration: elapsedTime,
        })
      }
    ).then(response => {
      if (response.status === 400){
        alert("The user_limit is out of range");
      }
      else if (response.status === 401){
        // redirect to login
        window.location.replace("/#/login");
      } else if (response.status === 403){
        alert("you naughty naughty")
      } else if (response.status === 200){
        alert("Successfully submitted solution")
        response.json().then(data => {
          console.log(data);
        })
      }
    })
  }

  const getExercise = async () =>{
    fetch(
      "/exercise?exercise_type=3&exercise_limit=19", 
      {
        method: "GET",
        headers: {"Content-Type": "application/json"},
      }
    ).then(response =>{
      if (response.status === 401){
        // redirect to login
        window.location.replace("/#/login");
      } else if (response.status === 403){
        console.log("No admin rights")
      } else if (response.status === 400){
        console.log("user_limit out of range")
      } else if (response.status === 200){
        response.json().then((data) => {
          // using static test data for now as data type is not disccused yet
          itemsRight = [];
          itemsLeft = [
            {id: 1, name: "# calculations"},
            {id: 2, name: "# input"},
            {id: 3, name: "import math"},
            {id: 4, name: "pi = (math.pi)"},
            {id: 5, name: "perimeter = 2*radius*pi"},
            {id: 6, name: "radius = input(\"Please enter the radius\""},
            {id: 7, name: "area = pi * radius * radius"},
            {id: 8, name: "print(radius, perimeter, area)"},
            {id: 9, name: "print(\"results:\""},
            {id: 10, name: "# output"}
          ];
          itemsLeftOriginal = itemsLeft.slice();
          console.log(data);
          exerciseID = data[1]["exercise_id"];
          exerciseTitle = data[1]["exercise_title"];
          exerciseDescription = data[1]["exercise_description"];
          exerciseContent = data[1]["exercise_content"];
        })
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
  
  startTimer();
  
  getExercise();
  
</script>

<Page title="Parsons Puzzle Exercise" fullwidth={true} requiredAccessLevel={accessLevels.user}>
  <div class="exercise-container">
    <div class="header-area">
      <h3>{exerciseTitle}</h3>
    </div>
    <div class="task-area">
      <TestCard />
    </div>
    <div class="puzzle-area">
      <PuzzleCard bind:itemsLeft bind:itemsRight />
    </div>
    <StatusBar {reset} {submitSolution}/>
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
</style>
