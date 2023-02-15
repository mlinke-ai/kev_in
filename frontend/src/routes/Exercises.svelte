<script lang="ts">
  import Page from "../lib/common/Page.svelte";
  import Card from "@smui/card";
  import Menu from "@smui/menu";
  import List, { Item, Separator, Text } from "@smui/list";
  import Button, { Label } from "@smui/button";
  import IconButton, { Icon } from "@smui/icon-button";
  import { Svg } from "@smui/common";

  import { each } from "svelte/internal";
  import { accessLevel } from "../stores";
  import { accessLevels } from "../lib/constants";

  let exercises = [];
  let currentExercise = 1;
  let maxDisplayedExercises = 20;
  let exercisesLoaded = false;

  let isAdmin = $accessLevel > accessLevels.user;

  const getExercises = async () => {
    fetch(`/exercise?exercise_offset=${currentExercise}`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          exercises = Object.values(data);
          console.log(exercises);
          currentExercise += maxDisplayedExercises;
          exercisesLoaded = true;
        });
      } else if (response.status === 400) {
        alert(this.message);
      } else if (response.status === 403) {
        alert(this.message);
      } else if (response.status === 500) {
        alert("Oops an Error occured. Please try again.");
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };

  getExercises();

  function showLastExercises() {
    currentExercise -= maxDisplayedExercises;
    exercisesLoaded = true;
    getExercises();
  }

  let menu: Menu;
  //this item needs ts (does not work with js)
</script>

<Page requiredAccessLevel={accessLevels.user}>
  <h1>Exercises</h1>

  {#if isAdmin}
    <div class="add-exercise">
      <Button on:click={() => menu.setOpen(true)}>
        <Icon component={Svg} viewBox="0 0 24 24">
          <path
            fill="outlined"
            d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9h-4v4h-2v-4H9V9h4V5h2v4h4v2z"
          />
        </Icon>
        <Label>add exercise</Label>
      </Button>

      <Menu bind:this={menu}>
        <List style="width: fit-content">
          <Item>
            <div class="display-icon">
              <Icon component={Svg} viewBox="-1 -11 45 45">
                <path
                  fill="outlined"
                  d="M20.5 11H19V7c0-1.1-.9-2-2-2h-4V3.5C13 2.12 11.88 1 10.5 1S8 2.12 8 3.5V5H4c-1.1 0-1.99.9-1.99 2v3.8H3.5c1.49 0 2.7 1.21 2.7 2.7s-1.21 2.7-2.7 2.7H2V20c0 1.1.9 2 2 2h3.8v-1.5c0-1.49 1.21-2.7 2.7-2.7 1.49 0 2.7 1.21 2.7 2.7V22H17c1.1 0 2-.9 2-2v-4h1.5c1.38 0 2.5-1.12 2.5-2.5S21.88 11 20.5 11z"
                />
              </Icon>
            </div>
            <p style="width: 175px;"><a href="/#/error">Parsons Puzzle</a></p>
            <!-- please insert link to create a parsons puzzle here -->
          </Item>
          <Item>
            <div class="display-icon">
              <Icon component={Svg} viewBox="0 -8 45 45">
                <path
                  fill="outlined"
                  d="M22 24H2v-4h20v4zM13.06 5.19l3.75 3.75L7.75 18H4v-3.75l9.06-9.06zm4.82 2.68-3.75-3.75 1.83-1.83c.39-.39 1.02-.39 1.41 0l2.34 2.34c.39.39.39 1.02 0 1.41l-1.83 1.83z"
                />
              </Icon>
            </div>
            <p style="width: 175px;">
              <a href="/#/error">Fill in the Blanks</a>
            </p>
            <!-- please insert link to create a fill in the blank here -->
          </Item>
          <Item>
            <div class="display-icon">
              <Icon component={Svg} viewBox="2 -6 35 35">
                <path
                  fill="outlined"
                  d="M9.4 16.6 4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0 4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"
                />
              </Icon>
            </div>
            <p style="width: 175px;">
              <a href="/#/error">Free Coding Exercise</a>
            </p>
            <!-- please insert link to create a free coding exercise here -->
          </Item>
        </List>
      </Menu>
    </div>
  {/if}

  <p>This is a placeholder site for listing all exercises.</p>

  {#if exercisesLoaded}
    <div class="grid-container">
      {#each exercises as exercise}
        <div class="grid-item">
            <a href="/#/error">
              <!-- please add link to display this exercise-->
              #{exercise.exercise_id}
              {exercise.exercise_title}
            </a>
            <p>
              {exercise.exercise_description}
            </p>
            <p>
              {exercise.exercise_type}
            </p>

            {#if isAdmin}
            <div style="display: flex; align-items: center;">
              <a href="/#/error">
                <!-- please add link to edit this exercise-->
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
            {/if}
        </div>
      {/each}
    </div>
  {/if}

  {#if isAdmin}
  <a href="/#/admin-dashboard">
    <Button>Back to dashboard</Button>
  </a>
  {:else}
  <a href="/#/user-dashboard">
    <Button>Back to dashboard</Button>
  </a>
  {/if}

  {#if exercises.length > maxDisplayedExercises && currentExercise == 1}
    <div class="list-exercises-buttons">
      <Button on:click={getExercises}>more users</Button>
    </div>
  {:else if exercises.length > maxDisplayedExercises && exercises.length <= currentExercise + maxDisplayedExercises - 1}
    <div class="list-exercises-buttons">
      <Button on:click={showLastExercises}>last users</Button>
    </div>
  {:else if exercises.length > maxDisplayedExercises && currentExercise != 1}
    <div class="list-exercises-buttons">
      <Button on:click={getExercises}>more users</Button>
      <Button on:click={showLastExercises}>last users</Button>
    </div>
  {/if}
  <!-- does not work properly yet, needs total number of exercises from backend-->
</Page>

<style>
  .grid-container {
    max-width: 3fr;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    background-color: rgb(0, 57, 49);
    padding: 10px;
    margin: auto auto;
    grid-auto-rows: auto;
    grid-gap: 10px;
  }

  .grid-item {
    word-break: break-all;
    width: minmax(350px, 1fr);
    background-color: #001a16;
    padding: 10px;
    font-size: 30px;
    text-align: center;
  }

  .add-exercise {
    float: right;
    align-items: center;
    /* margin-left: auto; */
    display: flex;
    width: fit-content;
  }

  .list-exercises-buttons {
    float: right;
  }

  .display-icon {
    margin-right: auto;
    width: 50px;
    height: 50px;
  }
</style>
