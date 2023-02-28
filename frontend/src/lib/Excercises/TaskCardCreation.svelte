<script>
  import UiCard from "../Common/UICard.svelte";
  import Textfield from '@smui/textfield';

  export let description = ""
</script>

<UiCard icon="school" title="Task">
  <div class="task-container">
    <textarea bind:value={description} class="input" placeholder="Describe your task using Markdown..."/>
  </div>
</UiCard>

<style lang="scss">
  .task-container {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      margin: 0 0.5rem 0.5rem 0.5rem;
      border-radius: 0.5rem;
      background-color: var(--console-background);;
      color: var(--console-color);;
      padding: 1rem;
      font-family: "Roboto Mono";
      overflow: auto;
  }

  .input {
    width: 99%;
    background-color: transparent;
    height: 98%;
    color: var(--console-color);
    border: none;
    resize: none;
    font-size: 1.5rem;;
  }

  .input:focus {
    outline: none !important;
    border-color: transparent;
  }
</style>
