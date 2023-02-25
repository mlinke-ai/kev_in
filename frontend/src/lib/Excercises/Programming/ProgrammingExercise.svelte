<script lang="ts">
  import Page from "../../Common/Page.svelte";
  import TaskCard from "../TaskCard.svelte";
  import CodingCard from "./CodingCard.svelte";
  import OutputCard from "./OutputCard.svelte";
  import StatusBar from "../StatusBar.svelte";
  import type { ProgrammingExerciseType } from "../types";
  import { submitSolution, getCurrentTimestamp, SolutionPostProgramming, SolutionGet } from "../solution";
  
  export let exerciseData: ProgrammingExerciseType;

  let elapsedTime = 0;
  let content: string = exerciseData.exercise_content.code;
  let solution: SolutionPostProgramming;
  let solutionResponse: SolutionGet;
  let serverMessage = "";
  let resetEditor: (content: string) => void;
  let focusEditor: () => void;

  async function submit() {
    solution = {
      solution_exercise: exerciseData.exercise_id,
      solution_date: getCurrentTimestamp(),
      solution_duration: elapsedTime,
      solution_content: {
        code: content
      }
    }
    solutionResponse = await submitSolution(solution);
    serverMessage = `Server>> ${solutionResponse.evaluator_message}`;
    if (solutionResponse.solution_correct) {
      // Do something cool
    } else {
      focusEditor()
    }
  }
  function reset() {
    resetEditor(exerciseData.exercise_content.code);
  }
</script>

<Page title="Coding Sandbox" fullwidth={true}>
  <div class="sandbox-container">
    <div class="header-area">
    </div>
    <div class="task-area">
      <TaskCard markdownSourceCode={exerciseData.exercise_description}/>
    </div>
    <div class="code-area">
      <CodingCard bind:content bind:focus={focusEditor} bind:reset={resetEditor} language={exerciseData.exercise_language_type} />
    </div>
    <div class="output-area">
      <OutputCard message={serverMessage}/>
    </div>
    <StatusBar bind:elapsedTime {reset} {submit} />
  </div>
</Page>

<style lang="scss">
  @use "../../../variables" as vars;

  * {
    box-sizing: border-box;
  }
  .sandbox-container {
    display: grid;
    grid-template-columns: 3fr 9fr;
    grid-template-rows: .5fr 9fr 2fr 0.5fr;
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
