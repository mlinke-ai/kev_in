<script lang="ts">
  import Fab, { Icon } from "@smui/fab";
  import Tooltip, { Wrapper } from "@smui/tooltip";
  import { selectedThemeIndex } from "../../stores";
  import ThemeButton from "./ThemeButton.svelte";
  import { themes, setTheme } from "./themes";

  function select(index) {
    if (index != $selectedThemeIndex) {
      $selectedThemeIndex = index;
      setTheme(themes[index], true);
    }
  }
</script>

<div class="theme-container">
  <div class="theme-scroll-area">
    {#each themes as theme, index}
      <ThemeButton
        on:click={() => select(index)}
        color={theme.dark["mdc-theme-primary"]}
        tooltip={theme.name}
        selected={index === $selectedThemeIndex}
      />
    {/each}
  </div>
  <Wrapper>
    <Fab on:click class="theme-mode-button" mini>
      <Icon style="color: white" class="material-icons">dark_mode</Icon>
    </Fab>
    <Tooltip style="z-index: 999;">Can't toggle darkmode</Tooltip>
  </Wrapper>
</div>

<style lang="scss">
  .theme-container {
    display: flex;
    align-items: center;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    gap: 0.5rem;
  }
  .theme-scroll-area {
    display: flex;
    align-items: center;
    // justify-content: center;
    gap: 0.2rem;
    cursor: grab;
    overflow-x: scroll;
    -webkit-overflow-scrolling: touch;
    touch-action: pan-x;
    max-width: 8rem;
    padding-top: 0.25rem;
    padding-bottom: 0.25rem;
    border-radius: 5rem;
    cursor: drag;
    -ms-overflow-style: none;
    scrollbar-width: none;

    ::-webkit-scrollbar {
      display: none;
    }
  }
  :global(.theme-mode-button) {
    // scale: 0.8;
    min-width: 2rem;
    min-height: 2rem;
    max-width: 2rem;
    max-height: 2rem;
    background-color: transparent;
    margin-left: auto;
  }
</style>
