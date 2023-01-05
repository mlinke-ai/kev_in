<script>
    import Button, { Icon, Label } from "@smui/button";
    import Card from "@smui/card";
</script>

<div class="output-container">
    <Card class="output-card">
        <div class="output-header">
            <div class="output-title">
                <Icon class="material-icons">terminal</Icon>
                <b>Output</b>
            </div>
        </div>
        <div class="output-area" />
    </Card>
</div>

<style lang="scss">
    .output-container {
        width: 100%;
        height: 100%;
    }
    * :global(.output-card) {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        border-radius: 1rem 1rem 0.5rem 0.5rem;
    }
    .output-header {
        padding: 0.7rem 1rem 0.7rem 1rem;
        display: flex;
        align-items: center;
    }
    .output-title {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    .output-area {
        height: 100%;
        margin: 0 0.5rem 0.5rem 0.5rem;
        border-radius: 0.5rem;
        background-color: black;
    }
</style>
