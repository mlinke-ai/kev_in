<script lang="ts">
  import Page from "../../lib/Common/Page.svelte";
  import Card from "@smui/card";
  import Menu from "@smui/menu";
  import List, { Item, Separator, Text } from "@smui/list";
  import Button, { Label } from "@smui/button";
  import IconButton, { Icon } from "@smui/icon-button";
  import { Svg } from "@smui/common";

  import { each } from "svelte/internal";
  import { exercises } from "../../lib/Excercises/types";

  let solutions = [];
  let exercises = [];
  let solutionsData;
  let solutionsMeta;
  const maxDisplayed = 18;
  let currentSolutionsUrl = `/solution?solution_offset=1&solution_limit=${maxDisplayed}`;
  let prevSolutionsUrl;
  let nextSolutionsUrl;
  let solutionsLoaded = false;

  const getSolutions = async () => {
    fetch(`${currentSolutionsUrl}`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          solutions = Object.values(data);
          console.log(solutions);
          solutionsData = Object.values(solutions[0]);
          solutionsMeta = Object.values(solutions[1]);
          console.log("solutionsData:");
          console.log(solutionsData);
          nextSolutionsUrl = solutionsMeta.next_url;
          prevSolutionsUrl = solutionsMeta.prev_url;
          getExercisesToSolutions();
          solutionsLoaded = true;
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

  function getExercisesToSolutions(){
    let requestUrl:string = `/exercise?`;
    console.log(solutionsData.length);
    solutionsData.forEach(element => {
      requestUrl += `exercise_id=${element.solution_exercise}&`;
    });
    requestUrl = requestUrl.slice(0, -1);
    getExercises(requestUrl);
    console.log(exercises.length)
  }

  const getExercises =async (requestUrl:string) => {
    fetch(`${requestUrl}`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
        console.log(data);
        exercises = Object.values(data);
        console.log(exercises);
        exercises = exercises[0];
        console.log("rightDataType?");
        console.log(exercises);
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

  <p>Look at all solutions you've handed in.</p>

  {#if solutionsLoaded}
    <div class="grid-container">
      {#each solutionsData as solution, index}
        <div class="grid-item">
          <Card>
            <a href="/#/error">
              <!-- please add link to display this solution-->

              #{solution.solution_id} - {index}
              <!-- add ${exercises[index]} if request to backend gives required data -->
            </a>
            <p>
              Handed in: {solution.solution_date}
            </p>

            {#if solution.solution_correct}
              <Icon class="material-icons">check</Icon>
            {:else}
              <Icon class="material-icons">clear</Icon>
            {/if}
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

  .list-solutions-buttons {
    float: right;
  }

  /* .display-icon {
    margin-right: auto;
    width: 50px;
    height: 50px;
  } */
</style>
