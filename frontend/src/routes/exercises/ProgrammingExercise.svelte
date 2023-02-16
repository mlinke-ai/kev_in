<script lang="ts">
  import Page from "../../lib/common/Page.svelte";
  import TaskCard from "../../lib/Excercises/TaskCard.svelte";
  import CodingCard from "../../lib/Excercises/Programming/CodingCard.svelte";
  import OutputCard from "../../lib/Excercises/Programming/OutputCard.svelte";
  import StatusBar from "../../lib/Excercises/StatusBar.svelte";
  import type { ProgrammingExerciseType } from "../../lib/Excercises/exercise";
  import { submitSolution, getCurrentTimestamp, SolutionPostProgramming } from "../../lib/Excercises/solution";

  let elapsedTime = 0;
  export let exerciseData: ProgrammingExerciseType;
  let content: string = exerciseData.exercise_content.code;
  let solution: SolutionPostProgramming;

  function submit() {
    solution = {
      solution_exercise: exerciseData.exercise_id,
      solution_date: getCurrentTimestamp(),
      solution_duration: elapsedTime,
      solution_content: {
        code: content
      }
    }
    submitSolution(solution);
  }
  function reset() {}
</script>

<Page title="Coding Sandbox" fullwidth={true}>
  <div class="sandbox-container">
    <div class="header-area">
      <h3>{exerciseData.exercise_title}</h3>
    </div>
    <div class="task-area">
      <TaskCard>
        {exerciseData.exercise_description}
      </TaskCard>
    </div>
    <div class="code-area">
      <CodingCard bind:content language={exerciseData.exercise_language} />
    </div>
    <div class="output-area">
      <OutputCard />
    </div>
    <StatusBar bind:elapsedTime {reset} {submit} />
  </div>
</Page>

<style lang="scss">
  @use "../../variables" as vars;

  * {
    box-sizing: border-box;
  }
  .sandbox-container {
    display: grid;
    grid-template-columns: 3fr 9fr;
    grid-template-rows: 1.5fr 8fr 2fr 0.5fr;
    grid-template-areas:
      "head head"
      "task code"
      "task out"
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
  }
  .code-area {
    grid-area: code;
    display: flex;
  }
  .output-area {
    grid-area: out;
    background-color: vars.$consoleBackground;
  }
</style>
