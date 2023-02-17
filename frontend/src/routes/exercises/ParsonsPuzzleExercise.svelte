<script lang="ts">
  import Page from "../../lib/common/Page.svelte";
  import PuzzleCard from "../../lib/Excercises/ParsonsPuzzle/PuzzleCard.svelte";
  import TaskCard from "../../lib/Excercises/TaskCard.svelte";
  import StatusBar from "../../lib/Excercises/StatusBar.svelte";
  import { accessLevels } from "../../lib/constants";
  import {
    SolutionPostParsonsPuzzle,
    submitSolution,
    getCurrentTimestamp
  } from "../../lib/Excercises/solution";
  import type { ParsonsPuzzleExerciseType } from "../../lib/Excercises/exercise";

  export let exerciseData: ParsonsPuzzleExerciseType;

  let solution: SolutionPostParsonsPuzzle;

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
    submitSolution(solution);
  }

  function reset() {
    itemsLeft = itemsLeftOriginal.slice();
    itemsRight = [];
  }
</script>

<Page
  title="Parsons Puzzle Exercise"
  fullwidth={true}
  requiredAccessLevel={accessLevels.user}
>
  <div class="exercise-container">
    <div class="header-area">
      <h3>{exerciseData.exercise_title}</h3>
    </div>
    <div class="task-area">
      <TaskCard />
    </div>
    <div class="puzzle-area">
      <PuzzleCard bind:itemsLeft bind:itemsRight />
    </div>
    <StatusBar {reset} {submit} bind:elapsedTime />
  </div>
</Page>

<style lang="scss">
  @use "../../variables" as vars;

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
