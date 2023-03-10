<script lang="ts">
  import Fab, { Icon } from "@smui/fab";
  import { SecondaryText } from "@smui/list";
  import Tooltip, { Wrapper } from "@smui/tooltip";
  import ThemeButton from "./ThemeButton.svelte";
  import { themes, setTheme, getTheme } from "./themes";

  let currentTheme = getTheme();

  function select(index) {
    if (index != currentTheme) {
      localStorage.setItem("preferredTheme", index);
      currentTheme = index;
      setTheme(index, true);
    }
  }
</script>

<div class="theme-container">
  <SecondaryText>Select theme</SecondaryText>
  <div class="theme-buttons">
    <div class="theme-scroll-area">
      {#each themes as theme, index}
        <ThemeButton
          on:click={() => select(index)}
          color={theme.dark["mdc-theme-primary"]}
          tooltip={theme.name}
          selected={index == currentTheme}
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
</div>

<style lang="scss">
  .theme-container {
    display: flex;
    flex-direction: column;
    align-items: start;
    padding: 0.5rem 1rem 0.5rem 1rem;
  }
  .theme-buttons {
    display: flex;
    align-items: center;
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
  }
  :global(.theme-mode-button) {
    // scale: 0.8;
    min-width: 2rem;
    min-height: 2rem;
    max-width: 2rem;
    max-height: 2rem;
    background-color: var(--mdc-theme-primary);
    margin-left: auto;
  }
</style>
