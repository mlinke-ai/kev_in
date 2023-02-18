<script>
  import UiCard from "../../common/UICard.svelte";
  import Textfield from "@smui/textfield";

  export let textPieces;
  export let userEntries;
</script>

<UiCard icon="extension" title="Puzzle">
  <div class="blanks-text-container">
    {#each textPieces as piece, i}
      {#if piece == "_"}
        <Textfield bind:value={userEntries[(i - 1) / 2]} class="textfield"/>
      {:else}
        {piece}
      {/if}
    {/each}
  </div>
</UiCard>

<style>
  .blanks-text-container {
    height: 70vh;
    width: 100%;
    overflow: scroll;
    padding: 1vh;
    line-height: 200%;
    font-size: large;
  }
  * :global(.textfield) {
    height: min-content;
  }
</style>
