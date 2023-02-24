<!-- Component to show output of code run on the server -->

<script>
    import UiCard from "../../Common/UICard.svelte";
</script>

<UiCard icon="terminal" title="Output">
    <div class="output-container">
        Server>>
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
        background-color: black;
        color: #7cfc00;
        font-family: "Roboto Mono";
    }
</style>
