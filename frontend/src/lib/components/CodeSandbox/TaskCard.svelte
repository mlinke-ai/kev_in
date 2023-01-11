<script>
    import Button, { Icon, Label } from "@smui/button";
    import Card from "@smui/card";
    import IconButton from "@smui/icon-button/src/IconButton.svelte";
</script>

<div class="task-container">
    <Card class="task-card">
        <div class="task-header">
            <div class="task-title">
                <Icon class="material-icons">school</Icon>
                <b>Task</b>
            </div>

            <div class="action-buttons">
                <IconButton>
                    <Icon class="material-icons md-icon">help</Icon>
                </IconButton>
            </div>
        </div>
        <div class="task-area">
            <h1>Welcome to your first test excercise!</h1>
            <p>
                To solve it you have to write a python script that prints out
                "Hello World".
            </p>
            <br />
            <hr />
            <br />
            Hints:
            <ul>
                <li>use the print() function</li>
                <li>strings have to be in quotation marks</li>
            </ul>
        </div>
    </Card>
</div>

<style lang="scss">
    @use "../../../variables" as vars;

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
        :last-child {
            margin-left: auto;
        }
    }
    .task-title {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    * :global(.md-icon) {
        padding: 0;
        margin: 0;
        color: vars.$primaryDark;
    }
    .task-area {
        height: 100%;
        margin: 0 0.5rem 0.5rem 0.5rem;
        border-radius: 0.5rem;
        background-color: vars.$consoleBackground;
        border: none;
        color: vars.$consoleColor;
        padding: 1rem;
        font-family: "Roboto Mono";
        overflow: scroll;
        hr {
            color: vars.$consoleColor;
        }
    }
</style>
