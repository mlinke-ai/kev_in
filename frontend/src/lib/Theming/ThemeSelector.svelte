<script lang="ts">
  import Button from "@smui/button";
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

<div class="theme-select-container">
  {#each themes as theme, index}
    <ThemeButton
      on:click={() => select(index)}
      color={theme.dark["mdc-theme-primary"]}
      tooltip={theme.name}
      selected={index === $selectedThemeIndex}
    />
  {/each}
</div>

<style>
  .theme-select-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding-top: .5rem;
    padding-bottom: .5rem;
  }
</style>
