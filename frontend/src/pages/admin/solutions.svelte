<script lang="ts">
  import Page from "../../lib/common/Page.svelte";
  import Card from "@smui/card";
  import Menu from "@smui/menu";
  import List, { Item, Separator, Text } from "@smui/list";
  import Button, { Label } from "@smui/button";
  import IconButton, { Icon } from "@smui/icon-button";
  import { Svg } from "@smui/common";

  import { each } from "svelte/internal";
  import { accessLevel } from "../../stores";
  import { accessLevels } from "../../lib/common/types";

  let solutions = [];
  let currentSolution = 1;
  let maxDisplayedSolutions = 20;
  let solutionsLoaded = false;

  let isAdmin = $accessLevel > accessLevels.user;
  console.log(isAdmin);

  const getSolutions = async () => {
    fetch(`/solution?solution_offset=${currentSolution}`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          console.log(data);
          solutions = Object.values(data);
          console.log(solutions);
          currentSolution += maxDisplayedSolutions;
          solutionsLoaded = true;
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

  getSolutions();

  function showLastSolutions() {
    currentSolution -= maxDisplayedSolutions;
    solutionsLoaded = true;
    getSolutions();
  }
</script>

<Page requiredAccessLevel={accessLevels.user}>
  <h1>Solutions</h1>

  <p>Look at all solutions you've handed in.</p>

  {#if solutionsLoaded}
    <div class="grid-container">
      {#each solutions as solution}
        <div class="grid-item">
          <Card>
            <a href="/#/error">
              <!-- please add link to display this solution-->
              #{solution.solution_id}
              {solution.solution_exercise}
            </a>
            <p>
              {solution.solution_date}{solution.solution_duration}
            </p>
            <p>
              needs to be evaluated: {solution.solution_pending}
              is correct: {solution.solution_correct}

            </p>
          </Card>
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

  {#if solutions.length > maxDisplayedSolutions && currentSolution == 1}
    <div class="list-solutions-buttons">
      <Button on:click={getSolutions}>more users</Button>
    </div>
  {:else if solutions.length > maxDisplayedSolutions && solutions.length <= currentSolution + maxDisplayedSolutions - 1}
    <div class="list-solutions-buttons">
      <Button on:click={showLastSolutions}>last users</Button>
    </div>
  {:else if solutions.length > maxDisplayedSolutions && currentSolution != 1}
    <div class="list-solutions-buttons">
      <Button on:click={getSolutions}>more users</Button>
      <Button on:click={showLastSolutions}>last users</Button>
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

  .list-solutions-buttons {
    float: right;
  }

  /* .display-icon {
    margin-right: auto;
    width: 50px;
    height: 50px;
  } */
</style>
