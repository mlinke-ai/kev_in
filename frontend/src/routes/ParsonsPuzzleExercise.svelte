<script>
  import {dndzone} from "svelte-dnd-action";
  import Page from "../lib/components/common/Page.svelte";
  import PuzzleCard from "../lib/components/Excercises/ParsonsPuzzle/PuzzleCard.svelte";
  import { userName } from "../stores";

  import TaskCard from "../lib/components/Excercises/TaskCard.svelte";
  import StatusBar from "../lib/components/Excercises/StatusBar.svelte";
  import { accessLevels } from "../lib/types";

  let itemsLeft = [];
  let itemsLeftOriginal = [];
  let itemsRight = [];
  let exerciseID = null;
  let exerciseTitle = "Exercise";
  let exerciseDescription = "Please use your Brain"


  function getCurrentTimestamp () {
    return Date.now()
  }

  const submitSolution = async () =>{
    fetch(
      "/solution",
      {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          solution_exercise: exerciseID,
          solution_date: 1675621950,
          solution_duration: elapsedTime,
          solution_content: JSON.stringify(itemsRight.map(item => item.name))
        })
      }
    ).then(response => {
      if (response.status === 400){
        alert("A required argument was not sent");
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
      "/exercise?exercise_type=3&exercise_limit=1&exercise_details=True&exercise_title=hallo", 
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
        response.json().then(data => {
          console.log(data)
          // using static test data for now as data type is not disccused yet
          itemsRight = [];
          let exerciseData = Object.values(data)[0]
          console.log(exerciseData)
          let exerciseContent = JSON.parse(exerciseData["exercise_content"])
          console.log(exerciseContent)
          for(let i = 0; i < exerciseContent.length; i++){
            itemsLeft[i] = {id: i+1, name: exerciseContent[i]}
          }
          itemsLeftOriginal = itemsLeft.slice();
          console.log(itemsLeft);
          exerciseTitle = exerciseData["exercise_title"];
          exerciseDescription = exerciseData["exercise_description"];
          exerciseID = exerciseData["exercise_id"]
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
      <TaskCard />
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
