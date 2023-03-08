<!-- Unified UI Card element with custom Title and content -->
<script lang="ts">
  import { Icon } from "@smui/button";
  import Card from "@smui/card";
  import IconButton from "@smui/icon-button";
  import type { UICardActionInterface } from "./types";

  export let title = "";
  export let icon = "";
  export let actions: Array<UICardActionInterface> = [];
</script>

<div class="uicard-container">
  <Card class="uicard">
    <div class="uicard-header">
      <div class="uicard-title">
        <Icon class="material-icons">{icon}</Icon>
        <b>{title}</b>
      </div>
      <div class="uicard-action-buttons">
        {#each actions as action}
            <IconButton on:click={action.func} class="material-icons">{action.icon}</IconButton>
        {/each}
      </div>
    </div>
    <div class="uicard-content-container">
      <slot />
    </div>
  </Card>
</div>

<style lang="scss">
  * {
    box-sizing: border-box;
  }
  * :global(.uicard-action-buttons) {
    color: var(--mdc-theme-primary);
  }
  .uicard-container {
    width: 100%;
    height: 100%;
  }
  * :global(.uicard) {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    border-radius: 1rem 1rem 0.5rem 0.5rem;
  }
  * :global(.uicard):focus-within {
    filter: drop-shadow(0px 0px 5px var(--mdc-theme-primary));
  }
  .uicard-header {
    padding: 0.7rem 1rem 0.7rem 1rem;
    display: flex;
    align-items: center;
    :last-child {
      margin-left: auto;
    }
  }
  .uicard-title {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
  .uicard-content-container {
    width: 100%;
    height: 100%;
    position: relative;
  }
</style>
