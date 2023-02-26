<script lang="ts">
  import Page from "../../lib/Common/Page.svelte";
  import Card from "@smui/card";
  import Menu from "@smui/menu";
  import List, { Item, Separator, Text } from "@smui/list";
  import Button, { Label } from "@smui/button";
  import IconButton, { Icon } from "@smui/icon-button";
  import { Svg } from "@smui/common";

  import { each } from "svelte/internal";
  import { accessLevel } from "../../stores";
  import { accessLevels } from "../../lib/Common/types";
  import { exercises } from "../../lib/Excercises/types";

  let solutions = [];
  let solutionsData;
  let solutionsMeta;
  const maxDisplayed = 18;
  let currentSolutionsUrl = `/solution?solution_offset=1&solution_limit=${maxDisplayed}`;
  let prevSolutionsUrl;
  let nextSolutionsUrl;
  let solutionsLoaded = false;

  //let isAdmin = $accessLevel > accessLevels.user;

  const getSolutions = async () => {
    fetch(`${currentSolutionsUrl}`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          solutions = Object.values(data);
          solutionsData = solutions[0];
          solutionsMeta = solutions[1];
          nextSolutionsUrl = solutionsMeta.next_url;
          prevSolutionsUrl = solutionsMeta.prev_url;

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
      {#each solutionsData as solution}
        <div class="grid-item">
          <Card>
            <a href="/#/error">
              <!-- please add link to display this solution-->
              {#if solution.solution_correct}
              {solution.solution_id}
              {exercises[solution.solution_exercise]}
              {/if}
            </a>
            <p>
              {solution.solution_date}{solution.solution_duration}
            </p>
            <p id=""></p>
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
