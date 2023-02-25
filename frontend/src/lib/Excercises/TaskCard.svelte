<script>
    import UiCard from "../Common/UICard.svelte";
    import showdown from "showdown";

    export let markdownSourceCode = "";

    let converter = new showdown.Converter();
    converter.setOption("tables", "true");
    converter.setFlavor("github");
    let renderedMD = converter.makeHtml(markdownSourceCode);
  </script>

<UiCard icon="school" title="Task">
    <div class="task-container">
      {@html renderedMD}
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
        background-color: var(--console-background);
        color: var(--console-color);
        padding: 1rem;
        font-family: "Roboto Mono";
        overflow: auto;
        font-size: 1.5rem;
    }
</style>
