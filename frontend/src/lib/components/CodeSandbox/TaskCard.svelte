<script>
    import Button, { Icon, Label } from "@smui/button";
    import Card from "@smui/card";
</script>

<div class="task-container">
    <Card class="task-card">
        <div class="task-header">
            <div class="task-title">
                <Icon class="material-icons">school</Icon>
                <b>Task</b>
            </div>
        </div>
        <div class="task-area">
            <div class="task-iframe">
                <p>Welcome to your first test excercise!</p>
                To solve it you have to write a python script that prints out "Hello World".
                <p>To print content in python you can use the <b>print()</b> function.</p>
                Put the text to print between the parantheses in quotation marks.
            </div>
        </div>
    </Card>
</div>

<style lang="scss">
    * {
        box-sizing: border-box;
    }
    .task-container {
        width: 100%;
        height: 100%;
    }
    * :global(.task-card) {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        border-radius: 1rem 1rem 0.5rem 0.5rem;
    }
    .task-header {
        padding: 0.7rem 1rem 0.7rem 1rem;
        display: flex;
        align-items: center;
    }
    .task-title {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    .task-area {
        height: 100%;
        margin: 0 0.5rem 0.5rem 0.5rem;
    }
    .task-iframe {
        height: 100%;
        width: 100%;
        border-radius: 0.5rem;
        background-color: black;
        border: none;
        color: #7CFC00;
        padding: 1rem;
        font-family: "Roboto Mono";
    }
</style>
