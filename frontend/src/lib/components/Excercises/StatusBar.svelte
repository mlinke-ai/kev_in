<script>
  import Button from "@smui/button/src/Button.svelte";
  import { Icon } from "@smui/common";
  export let reset;
  export let submitSolution;

  let startTime = 0;
  let elapsedTime = 0;
  let intervallID;
  const startTimer = () => {
    startTime = Date.now();
    intervallID = setInterval(() => {
      const endTime = Date.now();
      elapsedTime = endTime - startTime;
    })
  }

  const resetTimer = () => {
    elapsedTime = 0;
    clearInterval(intervallID);
  }
  
  let maxTimeReached = false;
  const format = (min, sec) => {
    // format to 2 digits and if maximum of 59 minutes and 59 seconds is reached, stop it
    if (maxTimeReached || min >= 59 && sec >= 59){
      maxTimeReached = true;
      return "59:59";
    }
    else {
      return ("00"+min.toString()).slice(-2) + ":" + ("00"+sec.toString()).slice(-2);
    }
  }
  $: seconds = (Math.floor(elapsedTime / 1000) % 60);
  $: minutes = (Math.floor(elapsedTime / 1000 / 60) % 60);
  $: formattedTime = format(minutes, seconds);
  
  startTimer();
</script>

<div class="status-bar">
  Getting Started - Attempt 1
  <div>
    <Button variant="outlined" on:click={reset}>Reset</Button>
    <Button variant="raised" on:click={() => submitSolution("1")}>
      Submit
    </Button>
  </div>
  <div class="clock-widget">
    {formattedTime}
    <Icon class="material-icons">access_time</Icon>
  </div>
</div>

<style lang="scss">
  @use "../../../variables" as vars;
  .status-bar {
    grid-area: status;
    color: vars.$consoleColor;
    font-family: "Roboto Mono";
    display: flex;
    align-items: center;
    gap: auto;
    justify-content: space-between;
  }
  .clock-widget {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
</style>
