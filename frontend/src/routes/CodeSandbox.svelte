<script>
  import Page from "../lib/components/common/Page.svelte";
  import AceEditor from "../lib/components/CodeSandbox/AceEditor.svelte";
  import OutputConsole from "../lib/components/CodeSandbox/OutputConsole.svelte";
  import TaskCard from "../lib/components/CodeSandbox/TaskCard.svelte";
  import TestCard from "../lib/components/CodeSandbox/TestCard.svelte";
  import { Icon } from "@smui/common";
    import CodingCard from "../lib/components/CodeSandbox/CodingCard.svelte";
    import OutputCard from "../lib/components/CodeSandbox/OutputCard.svelte";

  async function validate_code() {

  }
</script>

<Page title="Coding Sandbox" fullwidth={true}>
  <div class="sandbox-container">
    <div class="task-area">
      <TestCard />
    </div>
    <div class="code-area">
      <CodingCard />
    </div>
    <div class="output-area">
      <OutputCard />
    </div>
    <div class="status-bar">
      Getting Started - Attempt 1
      <div class="clock-widget">
        00:00
        <Icon class="material-icons">access_time</Icon>
      </div>
    </div>
  </div>
</Page>

<style lang="scss">
  * {
    box-sizing: border-box;
  }
  .sandbox-container {
    display: grid;
    grid-template-columns: 3fr 9fr;
    grid-template-rows: 8fr 3.5fr 0.5fr;
    grid-template-areas:
      "task code"
      "task out"
      "status status";
    gap: 1%;
    padding: 1rem 1rem 0.5rem 1rem;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background-color: black;
    // margin-left: 3%;
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
  .status-bar {
    grid-area: status;
    color: #7cfc00;
    font-family: "Roboto Mono";
    display: flex;
    align-items: center;
    :last-child {
      margin-left: auto;
    }
  }
  .clock-widget {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
</style>
