<script>
  import {dndzone} from "svelte-dnd-action";
  import Page from "../lib/common/Page.svelte";
  import PuzzleCard from "../lib//Excercises/ParsonsPuzzle/PuzzleCard.svelte";
  import { userName } from "../stores";

  import TaskCard from "../lib/Excercises/TaskCard.svelte";
  import StatusBar from "../lib/Excercises/StatusBar.svelte";
  import { accessLevels } from "../lib/constants";
  import { submitSolution } from "../lib/Excercises/exercise"

  let itemsLeft = [];
  let itemsLeftOriginal = [];
  let itemsRight = [];
  let exerciseID = null;
  let exerciseTitle = "Exercise";
  let exerciseDescription = "Please use your Brain"

  let elapsedTime;

  function submit() {
    submitSolution(exerciseID, elapsedTime, {list: itemsRight.map(item => item.name)})
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
        alert("No admin rights")
      } else if (response.status === 400){
        alert("user_limit out of range")
      } else if (response.status === 200){
        response.json().then(data => {
          // using static test data for now as data type is not disccused yet
          itemsRight = [];
          let exerciseData = Object.values(data)[0]
          let exerciseContent = exerciseData["exercise_content"]["list"]
          for(let i = 0; i < exerciseContent.length; i++){
            itemsLeft[i] = {id: i+1, name: exerciseContent[i]}
          }
          itemsLeftOriginal = itemsLeft.slice();
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
    <StatusBar {reset} {submit} bind:elapsedTime/>
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
