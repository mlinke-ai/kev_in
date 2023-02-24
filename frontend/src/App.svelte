<script lang="ts">
  import { prepareApp } from "./lib/Authentication/user";
  import { Router } from "@roxi/routify";
  import { routes } from "../.routify/routes";
  import CircularProgress from "@smui/circular-progress";
  import { setTheme } from "./lib/Theming/themes";

  let preferredTheme: number = localStorage.getItem("preferredTheme") as unknown as number
  if (preferredTheme == undefined) {
    preferredTheme = 1
    localStorage.setItem("preferredTheme", preferredTheme)
  }

  setTheme(preferredTheme, true)
</script>

{#await prepareApp()}
  <div class="loader">
    <CircularProgress
      style="width: 150px; height: 150px"
      class="circular-progress"
      indeterminate
    />
  </div>
{:then}
  <Router config={{ useHash: true, dynamicImports: false }} {routes} />
{/await}

<style>
  .loader {
    display: flex;
    justify-content: center;
    position: absolute;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
</style>
