<script lang="ts">
  import Page from "../../lib/Common/Page.svelte";
  import Card from "@smui/card";
  import Button, { Label } from "@smui/button";
  import IconButton, { Icon } from "@smui/icon-button";
  import { each } from "svelte/internal";

  let solutions = [];
  let exercises = [];
  let idxExToSol = []; //contains indizes of solution_exercises in exercises
  let solutionsData;
  let solutionsMeta;
  const maxDisplayed = 18;
  let currentSolutionsUrl = `/solution?solution_offset=1&solution_limit=${maxDisplayed}`;
  let prevSolutionsUrl;
  let nextSolutionsUrl;
  let solutionsLoaded = false;

  enum exerciseIcons {
    border_color,
    abc,
    extension,
    bug_report,
    assignment,
    terminal,
    code,
  }

  const getSolutions = async () => {
    fetch(`${currentSolutionsUrl}`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          solutions = Object.values(data);
          solutionsData = Object.values(solutions[0]);
          solutionsMeta = Object.values(solutions[1]);
          nextSolutionsUrl = solutionsMeta.next_url;
          prevSolutionsUrl = solutionsMeta.prev_url;
          getExercisesToSolutions();
        });
      } else if (response.status === 204) {
        alert("No one has a solution handed in yet :(");
      } else if (response.status === 403) {
        alert(response.status);
      } else if (response.status === 500) {
        alert("Oops an Error occured. Please try again.");
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };

  getSolutions();

  function getExercisesToSolutions() {
    let requestUrl: string = `/exercise?`;
    solutionsData.forEach((element) => {
      requestUrl += `exercise_id=${element.solution_exercise}&`;
    });
    requestUrl = requestUrl.slice(0, -1);
    getExercises(requestUrl);
  }

  const getExercises = async (requestUrl: string) => {
    fetch(`${requestUrl}`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          exercises = Object.values(data);
          exercises = exercises[0];
          orderExercisesToSolutions();
        });
      } else if (response.status === 403) {
        alert(response.status);
      } else if (response.status === 500) {
        alert("Oops an Error occured. Please try again.");
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };

  function orderExercisesToSolutions() {
    solutionsData.forEach((solution) => {
      let index = 0;
      exercises.forEach((exercise) => {
        if (solution.solution_exercise == exercise.exercise_id) {
          idxExToSol.push(index);
        }
        index++;
      });
    });
    solutionsLoaded = true;
  }

  function showLastSolutions() {
    solutionsLoaded = false;
    currentSolutionsUrl = prevSolutionsUrl;
    getSolutions();
  }

  function showNextSolutions() {
    solutionsLoaded = false;
    currentSolutionsUrl = nextSolutionsUrl;
    getSolutions();
  }
</script>

<Page>
  <h1>Solutions</h1>

  <p>Look at all solutions anyone has handed in.</p>

  {#if solutionsLoaded}
    <div class="grid-container">
      {#each solutionsData as solution, index}
        <div class="grid-item">
          <Card>
            <div class="card-grid">
              <div class="card-grid-icon">
                <Icon class="material-icons" style="transform: scale(2)">
                  {exerciseIcons[
                    exercises[idxExToSol[index]].exercise_type_value - 1
                  ]}
                </Icon>
              </div>

              <div class="card-grid-title">
                <a href="/#/error">
                  <!-- please add link to display this solution-->
                  #{solution.solution_id}
                  {exercises[idxExToSol[index]].exercise_title}
                </a>
              </div>
              <div class="card-grid-correct">
                {#if solution.solution_correct}
                  <Icon class="material-icons">check</Icon>
                {:else}
                  <Icon class="material-icons">clear</Icon>
                {/if}
              </div>

              <div class="card-grid-data">
                Handed in: {solution.solution_date}
              </div>
            </div>
          </Card>
        </div>
      {/each}
    </div>
  {/if}

  <a href="/#/admin">
    <Button>Back to dashboard</Button>
  </a>

  {#if prevSolutionsUrl == null && nextSolutionsUrl != null}
    <div class="list-solutions-buttons">
      <Button on:click={showNextSolutions}>more solutions</Button>
    </div>
  {:else if prevSolutionsUrl != null && nextSolutionsUrl == null}
    <div class="list-solutions-buttons">
      <Button on:click={showLastSolutions}>last solutions</Button>
    </div>
  {:else if prevSolutionsUrl != null && nextSolutionsUrl != null}
    <div class="list-solutions-buttons">
      <Button on:click={showLastSolutions}>last solutions</Button>
      <Button on:click={showNextSolutions}>more solutions</Button>
    </div>
  {/if}
</Page>

<style lang="scss">
  .grid-container {
    max-width: 3fr;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    background-color: transparent;
    padding: 10px;
    margin: auto auto;
    grid-auto-rows: auto;
    grid-gap: 10px;
  }

  .grid-item {
    word-break: break-all;
    width: minmax(350px, 1fr);
    background-color: var(--mdc-theme-primary);
    padding: 10px;
    font-family: monospace;
    text-align: center;
  }

  .card-grid {
    display: grid;
    grid-template-areas:
      "left right right"
      "menu main main";
    gap: 2px;
  }

  // .card-grid > div {
  //   background-color: rgba(255, 255, 255, 0.5);
  // }

  .card-grid-icon {
    margin: 10px;
    grid-area: left;
  }

  .card-grid-title {
    font-size: 24pt;
    padding: 10px;
    grid-area: right;
  }

  .card-grid-data {
    font-size: 18pt;
    padding: 10px;
    text-align: center;
    grid: main;
  }
  .card-grid-correct {
    margin: 10px;
    grid: menu;
  }

  .list-solutions-buttons {
    float: right;
  }
</style>
