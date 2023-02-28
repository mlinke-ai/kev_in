<script>
  import UiCard from "../../Common/UICard.svelte";
  import Textfield from "@smui/textfield";

  export let textPieces;
  export let userEntries;
</script>

<UiCard icon="article" title="Fill in the Blanks">
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
    width: 70vw;
    overflow: scroll;
    padding: 1vh;
    padding-left: 1.25rem;
    line-height: 200%;
    font-size: large;
  }

  * :global(.textfield) {
    height: min-content;
  }
</style>
