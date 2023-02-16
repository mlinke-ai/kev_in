<script lang="ts">
  import Page from "../lib/common/Page.svelte";
  import type {
    GetSolutionData,
    GetSolutionMeta,
  } from "../lib/Solutions/solution";
  import SolutionView from "../lib/Solutions/SolutionView/SolutionView.svelte";
  import {
    solutionData,
    solutionMeta,
  } from "../lib/Solutions/exampleSolutions";
</script>

<Page>
  <h3>User Solutions - Overview</h3>
  <!--<SolutionView {solutionData} {solutionMeta} />-->
  <iframe
    class="data-table-iframe"
    src="#/solution-view"
    title="standard"
  />
</Page>

<style>
  .data-table-iframe {
    height: 50vh;
    width: 35%;
    border: 1px solid
      var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.1));
  }
</style>