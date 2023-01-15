<script>
    import UiCard from "../common/UICard.svelte";
</script>

<UiCard icon="school" title="Task">
    <div class="task-container">
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
        hr {
            color: #7cfc00;
        }
    }
</style>
