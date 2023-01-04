<script>
  import Page from "../lib/components/common/Page.svelte";
</script>

<Page title="Coding Sandbox" fullwidth={true}>
  <div class="sandbox-container">
    <div class="navbar-container">Hello<br>
      World
    </div>
    <div class="task-area"></div>
    <div class="code-area"></div>
    <div class="output-area"></div>
  </div>
</Page>

<!--
import CodeBox from "../lib/components/common/CodeBox.svelte";
</script>

<Page title="Coding Sandbox" fullwidth={true}>
  <div class="coding-sandbox">
    <main>
      <CodeBox />
    </main>
    <aside>
      <div class="console-output" />
    </aside>
  </div>
</Page>

<style>
  .coding-sandbox {
    display: grid;
  }
  aside {
    position: absolute;
    right: 0;
    background-color: black;
  }
  
</style>
-->

<style lang="scss">
  .navbar-container {
    grid-area: nav;
    background-color: green;
    height: 100vh;
  }
  .task-area {
    grid-area: task;
    background-color: red;
  }
  .code-area {
    grid-area: code;
    background-color: black;
  }
  .output-area {
    grid-area: out;
    background-color: blue;
  }

  .sandbox-container {
    display: grid;
    grid-template-columns: 5% 25% 70%;
    grid-template-rows: auto;
    grid-template-areas:
      "nav task code"
      "nav task code"
      "nav task code"
      "nav task out";
  }
</style>
