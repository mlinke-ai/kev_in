<script lang="ts">
  import DataTable, {
    Head,
    Body,
    Row,
    Cell,
    Pagination,
  } from "@smui/data-table";
  import Select, { Option } from "@smui/select";
  import IconButton from "@smui/icon-button";
  import { Label } from "@smui/common";
  import type { GetSolutionData, GetSolutionMeta } from "./solution";

  export let solutionData: Array<GetSolutionData>;
  export let solutionMeta: GetSolutionMeta;

  export let currentPage: number = 1;
  export let rowsPerPage: number = 10;
</script>

<DataTable stickyHeader table$aria-label="User list" style="height: 500px; width: 50%;">
  <Head>
    <Row>
      <Cell numeric>ID</Cell>
      <Cell numeric>User</Cell>
      <Cell numeric>Exercise</Cell>
      <Cell>Solved</Cell>
    </Row>
  </Head>
  <Body>
    {#each solutionData as solution (solution.solution_id)}
      <Row>
        <Cell numeric>{solution.solution_id}</Cell>
        <Cell>{solution.solution_user}</Cell>
        <Cell>{solution.solution_exercise}</Cell>
        <Cell>{solution.solution_correct}</Cell>
      </Row>
    {/each}
  </Body>
  <Pagination slot="paginate">
    <svelte:fragment slot="rowsPerPage">
      <Label>Rows Per Page</Label>
      <Select variant="outlined" bind:value={rowsPerPage} noLabel>
        <Option value={10}>10</Option>
        <Option value={25}>25</Option>
        <Option value={100}>100</Option>
      </Select>
    </svelte:fragment>
    <svelte:fragment slot="total">
      {solutionData[0].solution_id}-{solutionData[0].solution_id + rowsPerPage} of {solutionMeta.total}
    </svelte:fragment>

    <IconButton
      class="material-icons"
      action="first-page"
      title="First page"
      on:click={() => (currentPage = 0)}
      disabled={currentPage === 0}>first_page</IconButton
    >
    <IconButton
      class="material-icons"
      action="prev-page"
      title="Prev page"
      on:click={() => currentPage--}
      disabled={currentPage === 0}>chevron_left</IconButton
    >
    <IconButton
      class="material-icons"
      action="next-page"
      title="Next page"
      on:click={() => currentPage++}
      disabled={currentPage === solutionMeta.pages}>chevron_right</IconButton
    >
    <IconButton
      class="material-icons"
      action="last-page"
      title="Last page"
      on:click={() => (currentPage = solutionMeta.pages)}
      disabled={currentPage === solutionMeta.pages}>last_page</IconButton
    >
  </Pagination>
</DataTable>

<style>
  /* Reset some of the demo app styles that interfere. */
  :global(body),
  :global(html) {
    height: auto;
    width: auto;
    position: static;
  }
  :global(#smui-app) {
    display: block;
    height: auto;
    overflow: auto;
  }
</style>