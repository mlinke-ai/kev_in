<script lang="ts">
  import Page from "../../Common/Page.svelte";
  import TaskCard from "../TaskCard.svelte";
  import CodingCard from "./CodingCard.svelte";
  import OutputCard from "./OutputCard.svelte";
  import StatusBar from "../StatusBar.svelte";
  import type {
    ExerciseGetProgramming,
    SolutionPostProgramming,
  } from "./types";
  import type { SolutionGet } from "../types";
  import { submitSolution, getCurrentTimestamp } from "../solution";
  import Dialog, { Title, Content, Actions } from "@smui/dialog";
  import Button, { Label, Icon } from "@smui/button";
  import { startPage } from "../../../stores";

  export let exerciseData: ExerciseGetProgramming;

  let elapsedTime = 0;
  let content: string = exerciseData.exercise_content.code;
  let solution: SolutionPostProgramming;
  let solutionResponse: SolutionGet;
  let serverMessage = "";

  let resetEditor: (content: string) => void;
  let focusEditor: () => void;

  let errorMessage;
  let openCorrectDialog = false;

  async function submit() {
    solution = {
      solution_exercise: exerciseData.exercise_id,
      solution_date: getCurrentTimestamp(),
      solution_duration: elapsedTime,
      solution_content: {
        code: content,
      },
    };
    solutionResponse = await submitSolution(solution);
    serverMessage = `Server>> ${solutionResponse.evaluator_message}`;
    if (solutionResponse.solution_correct) {
      openCorrectDialog = true;
    } else {
      errorMessage.open();
      focusEditor();
    }
  }
  function reset() {
    resetEditor(exerciseData.exercise_content.code);
  }
</script>

<Page title="Coding Sandbox" fullwidth={true}>
  <div class="sandbox-container">
    <div class="header-area" />
    <div class="task-area">
      <TaskCard markdownSourceCode={exerciseData.exercise_description} />
    </div>
    <div class="code-area">
      <CodingCard
        bind:content
        bind:focus={focusEditor}
        bind:reset={resetEditor}
        language={exerciseData.exercise_language_type}
      />
    </div>
    <div class="output-area">
      <OutputCard message={serverMessage} />
    </div>
    <StatusBar bind:elapsedTime {reset} {submit} />
  </div>
  <Dialog
    bind:open={openCorrectDialog}
    scrimClickAction=""
    escapeKeyAction=""
    aria-labelledby="mandatory-title"
    aria-describedby="mandatory-content"
  >
    <Title id="mandatory-title">Congratulations!</Title>
    <Content id="mandatory-content">You solved that task correctly!</Content>
    <Actions>
      <Button
        variant="outlined"
        on:click={() => {
          history.pushState({}, null, `#${$startPage}`);
        }}
      >
        <Icon class="material-icons">arrow_back</Icon>
        <Label>Return to Overview</Label>
      </Button>
    </Actions>
  </Dialog>
</Page>

<style lang="scss">
  @use "../../../variables" as vars;

  * {
    box-sizing: border-box;
  }
  .sandbox-container {
    display: grid;
    grid-template-columns: 3fr 9fr;
    grid-template-rows: 0.5fr 9fr 2fr 0.5fr;
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
