<script lang="ts">
  import Button from "@smui/button";
  import Page from "../../../lib/Common/Page.svelte";
  import CodingCard from "../../../lib/Excercises/Programming/CodingCard.svelte";
  import TaskCardCreation from "../../../lib/Excercises/TaskCardCreation.svelte";
  import Textfield from "@smui/textfield";
  import TestCaseCard from "../../../lib/Excercises/Programming/create/TestCaseCard.svelte";
  import type { TestCase } from "../../../lib/Excercises/Programming/create/types";
  import {
    exercises,
    ProgrammingPostExerciseType,
  } from "../../../lib/Excercises/types";
  import { postExercise } from "../../../lib/Excercises/exercise";
  import UiCard from "../../../lib/Common/UICard.svelte";
  import ParametersCard from "../../../lib/Excercises/Programming/create/ParametersCard.svelte";

  let exerciseTitle = "";
  let exerciseDescription = "";
  let code = "";
  let func = "";
  let testCases: Array<TestCase>;
  let solution: {
    [key: string]: [Array<number>, Array<number>];
  } = {};
  let exercise: ProgrammingPostExerciseType;

  function submit() {
    for (let i = 0; i < testCases.length; i++) {
      solution[i.toString()] = [testCases[i].input, testCases[i].output];
    }
    exercise = {
      exercise_title: exerciseTitle,
      exercise_description: exerciseDescription,
      exercise_type: exercises.programming,
      exercise_language: 1,
      exercise_content: {
        code: code,
        func: func,
      },
      exercise_solution: solution,
    };
    postExercise(exercise);
  }
</script>

<Page title="Create Programming Exercise" fullwidth={true}>
  <div class="exercise-container">
    <div class="header-area">
      <Textfield
        bind:value={exerciseTitle}
        label="Exercise Title"
        required
        style="width: 100%"
      />
      <Textfield
        bind:value={func}
        label="Function Name"
        required
        style="width: 100%"
      />
    </div>
    <div class="task-area">
      <TaskCardCreation bind:description={exerciseDescription} />
    </div>
    <div class="creation-area">
      <div class="coding-area">
        <CodingCard bind:content={code}/>
        <!--<ParametersCard />-->
      </div>
      <div style="width: 40%">
        <TestCaseCard bind:testCases />
      </div>
    </div>
    <div class="status-bar">
      Programming Exercise - Creation
      <div>
        <Button variant="outlined">Reset</Button>
        <Button variant="raised" on:click={submit}>Submit new Exercise</Button>
      </div>
    </div>
  </div>
</Page>

<style lang="scss">
  .coding-area {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: .5rem;
  }
  .exercise-container {
    display: grid;
    grid-template-columns: 3fr 9fr;
    grid-template-rows: auto 9fr auto;
    grid-template-areas:
      "head head"
      "task creation-area"
      "status status";
    gap: 0.5rem;
    height: 98vh;
    padding: 0.5rem 0.5rem 0.5rem 0.5rem;
  }

  .header-area {
    grid-area: head;
    height: max-content;
    display: flex;
    gap: 1rem;
  }
  .task-area {
    grid-area: task;
  }
  .creation-area {
    grid-area: creation-area;
    display: flex;
    gap: 0.5rem;
  }
  .status-bar {
    grid-area: status;
    color: var(--console-color);
    font-family: "Roboto Mono";
    display: flex;
    align-items: center;
    gap: auto;
    justify-content: space-between;
    height: max-content;
    padding-top: 0.5rem;
  }
</style>
