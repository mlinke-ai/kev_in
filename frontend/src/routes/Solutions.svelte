<script lang="ts">
  import Page from "../lib/common/Page.svelte";
  import type {
    GetSolutionData,
    GetSolutionMeta,
  } from "../lib/Solutions/solution";
  import SolutionView from "../lib/Solutions/SolutionView.svelte";
  import { solutionData, solutionMeta } from "../lib/Solutions/exampleSolutions"
</script>

<Page>
    <h3>User Solutions - Overview</h3>
    <SolutionView {solutionData} {solutionMeta} />
</Page>

