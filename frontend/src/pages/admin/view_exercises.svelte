<script lang="ts">
  import Page from "../../lib/common/Page.svelte";
  import Card from "@smui/card";
  import Menu from "@smui/menu";
  import List, { Item, Separator, Text } from "@smui/list";
  import Button, { Label } from "@smui/button";
  import IconButton, { Icon } from "@smui/icon-button";
  import { Svg } from "@smui/common";

  import { accessLevel, startPage } from "../../stores";
  import { accessLevels } from "../../lib/common/types";
  import { link } from "svelte-spa-router";

  let exercises = [];
  let exercisesData;
  let exercisesMeta;
  const maxDisplayed = 18;
  let currentExerciseUrl = `/exercise?exercise_offset=1&exercise_limit=${maxDisplayed}`;
  let nextExerciseUrl = null;
  let prevExerciseUrl = null;
  let exercisesLoaded = false;

  enum exerciseIcons{border_color, abc, extension, bug_report, assignment, terminal, code};

  let isAdmin = $accessLevel > accessLevels.user;

  const getExercises = async () => {
    fetch(`${currentExerciseUrl}`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          exercisesData = Object.values(data);
          exercises = exercisesData[0];
          exercisesMeta = exercisesData[1];
          nextExerciseUrl = exercisesMeta.next_url;
          prevExerciseUrl = exercisesMeta.prev_url;
          console.log(prevExerciseUrl);
          exercisesLoaded = true;
        });
      } else if (response.status === 204) {
        alert("No exercises in database. Please create some. Error: " + response.status);
      } else if (response.status === 400) {
        alert("Error: " + response.status + "\n Page limit not in range");
      } else if (response.status === 500) {
        alert("Oops an Error occured. Please try again.");
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };

  getExercises();

  function showLastExercises() {
    currentExerciseUrl = prevExerciseUrl;
    getExercises();
  }

  function showNextExercises(){
    currentExerciseUrl = nextExerciseUrl;
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
          <a use:link href="/admin/exercises/create/parsonspuzzle">
            <Item class="add-exercise-item">
              <Icon class="material-icons add-exercise-item-icon"
                >extension</Icon
              >
              <p style="width: 175px;">Parsons Puzzle</p>
            </Item>
          </a>
          <a use:link href="/error">
            <Item class="add-exercise-item">
              <Icon class="material-icons add-exercise-item-icon"
                >border_color</Icon
              >
              <p style="width: 175px;">Fill in the Blanks</p>
              <!-- please insert link to create a fill in the blank exercise here -->
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
            <div class="card-grid">
              <div class="card-grid-icon">
                  <Icon class="material-icons" style="transform: scale(2)">
                    {exerciseIcons[exercise.exercise_type_value -1]}
                  </Icon>
              </div>
              <div class="card-grid-title">
                #{exercise.exercise_id}
                {exercise.exercise_title}
              </div>
            
            <p class="card-grid-description">
              {exercise.exercise_description}
            </p>
          </div>
        </a>

            {#if isAdmin}
              <div style="display: flex; align-items: center;">
                <a href="/#/error">
                  <!-- please add link to edit this exercise-->
                    <Icon class="material-icons">
                      edit
                    </Icon>
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

  {#if prevExerciseUrl == null && nextExerciseUrl != null}
    <div class="list-exercises-buttons">
      <Button on:click={showNextExercises}>more exercises</Button>
    </div>
  {:else if prevExerciseUrl != null && nextExerciseUrl == null}
    <div class="list-exercises-buttons">
      <Button on:click={showLastExercises}>last exercises</Button>
    </div>
  {:else if prevExerciseUrl != null && nextExerciseUrl != null}
    <div class="list-exercises-buttons">
      <Button on:click={showLastExercises}>last exercises</Button>
      <Button on:click={showNextExercises}>more exercises</Button>
    </div>
  {/if}
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

  .card-grid{
    display: grid;
    grid-template-areas: 
    "left right right"
    "main main main";
  }

  .card-grid-icon{
    width: fit-content;
    padding:10px;
    grid-area: left;
  }

  .card-grid-title{
    padding: 10px;
    grid-area: right;
  }

  .card-grid-description{
    padding: 10px;
    grid: main;
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
