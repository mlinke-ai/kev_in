<script>
    import {flip} from "svelte/animate";
    import {dndzone} from "svelte-dnd-action";
    import Button from "@smui/button/src/Button.svelte";
    import Page from "../lib/components/common/Page.svelte";
    import { Icon } from "@smui/common";
    import PuzzleCard from "../lib/components/ParsonsPuzzleExercise/PuzzleCard.svelte";

    import TestCard from "../lib/components/CodeSandbox/TestCard.svelte";
    import CodingCard from "../lib/components/CodeSandbox/CodingCard.svelte";
    import OutputCard from "../lib/components/CodeSandbox/OutputCard.svelte";

    const getExercise = async () =>{
        fetch("/exercise?exercise_id=1", {method: "GET", headers: {"Content-Type": "application/json", "Cookie": "token=<token>"}})

    }

</script>

<Page title="Parsons Puzzle Exercise" fullwidth={true}>
    <div class="exercise-container">
      <div class="header-area">
        <h3>Parsons Puzzle Exercise</h3>
      </div>
      <div class="task-area">
        <TestCard/>
      </div>
      <div class="puzzle-area">
        <PuzzleCard/>
      </div>
      <div class="status-bar">
        Getting Started - Attempt 1
        <div class="clock-widget">
          00:00
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
    height: 600px;
  }
  .status-bar {
    grid-area: status;
    color: vars.$consoleColor;
    font-family: "Roboto Mono";
    display: flex;
    align-items: center;
    :last-child {
      margin-left: auto;
    }
  }
  .clock-widget {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
</style>

