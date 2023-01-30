<script>
  import Page from "../lib/components/common/Page.svelte";
  import Button from "@smui/button/src/Button.svelte";
  import Card, {
    Content,
    PrimaryAction,
    Media,
    MediaContent,
    Actions,
    ActionButtons,
    ActionIcons,
  } from "@smui/card";
  import EditSvg from "../lib/components/AnimatedSVG/EditSVG.svelte";
  //import { mdiFormatColorFill, mdiWrench, mdiCurrencyUsd } from '@mdi/js';
  import IconButton, { Icon } from "@smui/icon-button";
  import { Svg } from "@smui/common";
  import { each } from "svelte/internal";

  const exercises = [
    {
      exercise_id: 0,
      exercise_title: "example",
      exercise_description: "some description",
      exercise_type: 0,
      exercise_content: "1+1=",
      exercise_offset: 0,
      exercise_limit: 0,
    },
    {
      exercise_id: 1,
      exercise_title: "example2",
      exercise_description: "some other description",
      exercise_type: 0,
      exercise_content: "1+2=",
      exercise_offset: 0,
      exercise_limit: 0,
    },
    {
      exercise_id: 2,
      exercise_title: "example3",
      exercise_description: "some other description",
      exercise_type: 0,
      exercise_content: "3+2=",
      exercise_offset: 0,
      exercise_limit: 0,
    },
    //content only for testcases
    //turn later to
    //getExercises
  ];

  let currentExercise = 0;
  let maxDisplayedExercises = 3;

  const getExercises = async () => {
    await fetch(
      "http://127.0.0.1:5000/exercise?exercise_offset=currentExercise&exercise_limit=maxDisplayedExercises",
      {
        method: "GET",
      }
    ).then((response) => {
      if (response.status == 200) {
        while (exercises.length != 0) {
          exercises.pop();
        }
        exercises.push(this);
        currentExercise += exercises.length;
      } else if (response.status == 400) {
        alert(this.message);
      } else if (response.status == 403) {
        alert(this.message);
      } else if (response.status == 500) {
        alert("Oops an Error occured. Please try again.");
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };

  getExercises();

  function showLastExercises() {
    currentExercise -= exercises.length;
    getExercises();
  }
</script>

<Page>

  <div class="add-exercise-icon">
    <div style="display: flex; align-items: center;">
      <a href="/#/error">
        <IconButton>
          <Icon component={Svg} viewBox="0 0 24 24">
            <path
              fill="outlined"
              d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9h-4v4h-2v-4H9V9h4V5h2v4h4v2z"
            />
          </Icon>
        </IconButton>&nbsp; add exercise
      </a>
    </div>
  </div>

  <h1>Exercises</h1>

  <p>This is a placeholder site for listing all exercises.</p>

  <div class="grid-container">
    {#each exercises as exercise}
      <div class="grid-item">
        <Card>
          <a href="/#/error">
            #{exercise.exercise_id}
            {exercise.exercise_title}
          </a>
          <p>
            {exercise.exercise_description}
          </p>
          <p>
            {exercise.exercise_type}
          </p>

          <div style="display: flex; align-items: center;">
            <a href="/#/error">
              <IconButton>
                <Icon component={Svg} viewBox="0 0 24 24">
                  <path
                    fill="outlined"
                    d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a.9959.9959 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"
                  />
                </Icon>
              </IconButton>
            </a>
          </div>
        </Card>
      </div>
    {/each}
  </div>

  <!-- <div class="grid-container">
    <div class="grid-item">
        <Card>
        Exercise 01
        <div style="display: flex; align-items: center;">
            <a href="/#/error">
            <IconButton>
              <Icon component={Svg} viewBox="0 0 24 24">
                <path fill="outlined" 
                d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a.9959.9959 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
              </Icon>
            </IconButton>
        </a>
          </div>
        </Card>
    </div>
    <div class="grid-item">Exercise 02</div>
    <div class="grid-item">Exercise 03</div>
    <div class="grid-item">Exercise 04</div>
    <div class="grid-item">Exercise 05</div>
    <div class="grid-item">Exercise 06</div>
    <div class="grid-item">Exercise 07</div>
    <div class="grid-item">Exercise 08</div>
    <div class="grid-item">Exercise 09</div>
    <div class="grid-item">Exercise 10</div>
    <div class="grid-item">Exercise 11</div>
    <div class="grid-item">Exercise 12</div>
    <div class="grid-item">Exercise 13</div>
    <div class="grid-item">Exercise 14</div>
    <div class="grid-item">Exercise 15</div>
  </div> -->

  <a href="/#/admin-dashboard">
    <Button>Back to dashboard</Button>
  </a>

  

  {#if exercises.length < maxDisplayedExercises}

  <div class="list-exercises-buttons">
    <Button on:click={showLastExercises}>last exercises</Button>
  </div>

  {:else if exercises.length == maxDisplayedExercises && currentExercise == 0}

  <div class="list-exercises-buttons">
    <Button on:click={getExercises}>more exercises</Button>
  </div>

  {:else}

  <div class="list-exercises-buttons">
    <Button on:click={getExercises}>more exercises</Button>
    <Button on:click={showLastExercises}>last exercises</Button>
  </div>

  {/if}
  
</Page>

<style>
  .grid-container {
    display: grid;
    grid-template-columns: auto auto auto;
    background-color: rgb(0, 57, 49);
    padding: 10px;
  }

  .grid-item {
    width: 350px;
    background-color: #001a16;
    border: 1px solid rgba(0, 0, 0, 0.8);
    padding: 10px;
    font-size: 30px;
    text-align: center;
  }

  .add-exercise-icon {
    float: right;
    align-items: right;
  }

  .list-exercises-buttons{
    float: right;
  }
</style>
