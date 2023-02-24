<script lang="ts">
  import Tooltip, { Wrapper } from "@smui/tooltip";
  import Fab, { Icon } from "@smui/fab";
  export let color: string;
  export let tooltip: string;
  export let selected = false;
</script>

<Wrapper>
  <Fab
    class="theme-select-fab {selected ? 'selected' : ''}"
    on:click
    style={`background-color: ${color};`}
    mini
  >
    {#if selected}
      <Icon style="color: white" class="material-icons">check</Icon>
    {/if}
  </Fab>
  <Tooltip style="z-index: 999;">{tooltip}</Tooltip>
</Wrapper>

<style lang="scss">
  :global(.theme-select-fab) {
    // scale: 0.8;
    min-width: 2rem;
    min-height: 2rem;
    max-width: 2rem;
    max-height: 2rem;
  }
  :global(.selected) {
    border: 2px solid white;
  }
</style>
