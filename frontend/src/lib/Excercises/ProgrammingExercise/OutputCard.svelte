<!-- Component to show output of code run on the server -->

<script lang="ts">
    import UiCard from "../../Common/UICard.svelte";

    export let message: String;
</script>

<UiCard icon="terminal" title="Output">
    <div class="output-container">
        {message}
    </div>
</UiCard>

<style>
    .output-container {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        margin: 0 0.5rem 0.5rem 0.5rem;
        padding: 1rem;
        border-radius: 0.5rem;
        color: var(--console-color);
        background-color: var(--console-background);
        font-family: "Roboto Mono";
    }
</style>
