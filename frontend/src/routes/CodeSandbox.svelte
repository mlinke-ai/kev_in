<script>
  import Page from "../lib/components/common/Page.svelte";
  import AceEditor from "../lib/components/CodeSandbox/AceEditor.svelte";
  import OutputConsole from "../lib/components/CodeSandbox/OutputConsole.svelte";
  import TaskCard from "../lib/components/CodeSandbox/TaskCard.svelte";
</script>

<Page title="Coding Sandbox" fullwidth={true}>
  <div class="sandbox-container">
    <div class="task-area">
      <TaskCard />
    </div>
    <div class="code-area">
      <AceEditor />
    </div>
    <div class="output-area">
      <OutputConsole />
    </div>
  </div>
</Page>

<!--

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
  * {
    box-sizing: border-box;
  }
  .sandbox-container {
    display: grid;
    grid-template-columns: 5fr 14fr;
    grid-template-rows: auto;
    grid-template-areas:
      "task code"
      "task code"
      "task code"
      "task out";
    gap: 1%;
    padding: 1rem;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background-color: black;
    margin-left: 3%;
  }
  .task-area {
    grid-area: task;
  }
  .code-area {
    grid-area: code;
    display: flex;
  }
  .output-area {
    grid-area: out;
    background-color: black;
  }
</style>
