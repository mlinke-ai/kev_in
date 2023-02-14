<script>
  import Page from "../lib/common/Page.svelte";
  import TaskCard from "../lib/Excercises/TaskCard.svelte";
  import CodingCard from "../lib/Excercises/CodeSandbox/CodingCard.svelte";
  import OutputCard from "../lib/Excercises/CodeSandbox/OutputCard.svelte";
  import StatusBar from "../lib/Excercises/StatusBar.svelte";
  import { submitSolution } from "../lib/Excercises/exercise";

  let elapsedTime;
  let exerciseID = null;

  function submit() {
    submitSolution(exerciseID, elapsedTime, "code here")
  }
  function reset() {}
</script>

<Page title="Coding Sandbox" fullwidth={true}>
  <div class="sandbox-container">
    <div class="header-area">
      <h3>Coding Sandbox</h3>
    </div>
    <div class="task-area">
      <TaskCard>
        <h1>Welcome to your first test excercise!</h1>
        <p>
          To solve it you have to write a python script that prints out "Hello
          World".
        </p>
        <br />
        <hr />
        <br />
        Hints:
        <ul>
          <li>use the print() function</li>
          <li>strings have to be in quotation marks</li>
        </ul>
      </TaskCard>
    </div>
    <div class="code-area">
      <CodingCard />
    </div>
    <div class="output-area">
      <OutputCard />
    </div>
    <StatusBar bind:elapsedTime {reset} {submit}/>
  </div>
</Page>

<style lang="scss">
  @use "../variables" as vars;

  * {
    box-sizing: border-box;
  }
  .sandbox-container {
    display: grid;
    grid-template-columns: 3fr 9fr;
    grid-template-rows: 1.5fr 8fr 2fr 0.5fr;
    grid-template-areas:
      "head head"
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
  .header-area {
    grid-area: head;
    h3 {
      color: vars.$primaryDark;
    }
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
    background-color: vars.$consoleBackground;
  }
</style>
