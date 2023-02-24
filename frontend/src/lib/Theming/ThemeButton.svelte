<script lang="ts">
  import Tooltip, { Wrapper } from "@smui/tooltip";
  import Fab, { Icon } from "@smui/fab";
  export let color: string;
  export let tooltip: string;
  export let selected = false;
</script>

<Wrapper>
  <Fab on:click style={`background-color: ${color};`} on:click={() => {}} mini>
    {#if selected}
      <Icon style="color: white" class="material-icons">check</Icon>
    {/if}
  </Fab>
  <Tooltip>{tooltip}</Tooltip>
</Wrapper>
