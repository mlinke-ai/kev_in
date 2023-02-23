<script lang="ts">
  import Page from "../../lib/Common/Page.svelte";
  import Card from "@smui/card";
  import Menu from "@smui/menu";
  import List, { Item, Separator, Text } from "@smui/list";
  import Button, { Label } from "@smui/button";
  import IconButton, { Icon } from "@smui/icon-button";
  import { Svg } from "@smui/common";

  import { accessLevel, startPage } from "../../stores";
  import { accessLevels } from "../../lib/Common/types";
  import { link } from "svelte-spa-router";

  let exercises = [];
  let exercisesData;
  let exercisesMeta;
  let nextExerciseUrl = "/exercise?exercise_offset=1&exercise_page=1";
  //let maxDisplayedExercises = 20;
  let exercisesLoaded = false;

  let isAdmin = $accessLevel > accessLevels.user;

  const getExercises = async () => {
    fetch(`${nextExerciseUrl}`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          exercisesData = Object.values(data);
          exercises = exercisesData[0];
          exercisesMeta = exercisesData[1];
          nextExerciseUrl = exercisesMeta.next_url;
          console.log(nextExerciseUrl);
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
    // currentExercise -= maxDisplayedExercises;
    // exercisesLoaded = true;
    getExercises();
  }

  let menu: Menu;
  //this item needs ts (does not work with js)
</script>

<Page>
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
          <a use:link href="/error">
            <Item class="add-exercise-item">
              <Icon class="material-icons add-exercise-item-icon"
                >extension</Icon
              >
              <p style="width: 175px;">Parsons Puzzle</p>
              <!-- please insert link to create a free coding exercise here -->
            </Item>
          </a>
          <a use:link href="/error">
            <Item class="add-exercise-item">
              <Icon class="material-icons add-exercise-item-icon"
                >border_color</Icon
              >
              <p style="width: 175px;">Fill in the Blanks</p>
              <!-- please insert link to create a free coding exercise here -->
            </Item>
          </a>
          <a use:link href="/error">
            <Item class="add-exercise-item">
              <Icon class="material-icons add-exercise-item-icon">code</Icon>
              <p style="width: 175px;">Free Coding Exercise</p>
              <!-- please insert link to create a free coding exercise here -->
            </Item>
          </a>
        </List>
      </Menu>
    </div>
  {/if}

  <p>This is a placeholder site for listing all exercises.</p>

  {#if exercisesLoaded}
    <div class="grid-container">
      {#each exercises as exercise}
        <div class="grid-item">
          <Card>
            <a use:link href={`/exercises/${exercise.exercise_id}`}>
              #{exercise.exercise_id}
              {exercise.exercise_title}
            </a>
            <!-- <p>
              {exercise.exercise_description}
            </p> -->
            <p>
              {exercise.exercise_type_name}
            </p>

            {#if isAdmin}
              <div style="display: flex; align-items: center;">
                <a href="/#/error">
                  <!-- please add link to edit this exercise-->
                  <IconButton>
                    <Icon class="material-icons">
                      edit
                    </Icon>
                    <!-- <Icon component={Svg} viewBox="0 0 24 24">
                      <path
                        fill="outlined"
                        d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a.9959.9959 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"
                      />
                    </Icon> -->
                  </IconButton>
                </a>
              </div>
            {/if}
          </Card>
        </div>
      {/each}
    </div>
  {/if}
  <a use:link href={$startPage}>
    <Button>Back to dashboard</Button>
  </a>

  <!-- {#if exercises.length > maxDisplayedExercises && currentExercise == 1}
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
  {/if} -->
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

  * :global(.add-exercise-item) {
    display: flex;
    gap: 1rem;
  }

  * :global(.add-exercise-item-icon) {
    transform: scale(110%);
  }
</style>
