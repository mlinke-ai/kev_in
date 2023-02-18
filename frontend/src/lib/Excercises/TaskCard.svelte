<script>
    import UiCard from "../common/UICard.svelte";
    export let markdownSourceCode = "";


</script>

<UiCard icon="school" title="Task">
    <div class="task-container">
      <pre>{markdownSourceCode}</pre>
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
        background-color: black;
        color: #7cfc00;
        padding: 1rem;
        font-family: "Roboto Mono";
        overflow: auto;
    }
</style>
