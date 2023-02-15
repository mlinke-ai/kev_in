<script>
    import { dndzone } from "svelte-dnd-action";
    import Page from "../lib/common/Page.svelte";
    import BlanksCard from "../lib//Excercises/FillInBlanks/BlanksCard.svelte";
    import { userName } from "../stores";

    import TaskCard from "../lib/Excercises/TaskCard.svelte";
    import StatusBar from "../lib/Excercises/StatusBar.svelte";
    import { accessLevels } from "../lib/constants";

    let blankPositions = [];
    let textPieces = [];
    let userEntries = [];
    // Thats originaly from the parsons puzzle...
    // let itemsLeft = [];
    // let itemsLeftOriginal = [];
    // let itemsRight = [];
    let exerciseID = null;
    let exerciseTitle = "Exercise";
    let exerciseDescription = "Please use your Brain";

    // TODO fix this by adapting the Statusbar (bind)
    let elapsedTime = 0;

    function getCurrentTimestamp() {
        return Date.now() / 1000;
    }

    const submitSolution = async () => {
        fetch("/solution", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                solution_exercise: exerciseID,
                solution_date: getCurrentTimestamp(),
                solution_duration: elapsedTime,
                solution_content: {
                    list: itemsRight.map((item) => item.name),
                },
            }),
        }).then((response) => {
            if (response.status === 400) {
                alert("A required argument was not sent");
            } else if (response.status === 401) {
                // redirect to login
                window.location.replace("/#/login");
            } else if (response.status === 403) {
                alert("you naughty naughty");
            } else if (response.status === 200) {
                alert("Successfully submitted solution");
                response.json().then((data) => {
                    console.log(data);
                });
            }
        });
    };

    const getExercise = async () => {
        fetch(
            "/exercise?exercise_type=3&exercise_limit=1&exercise_details=True&exercise_title=hallo",
            {
                method: "GET",
                headers: { "Content-Type": "application/json" },
            }
        ).then((response) => {
            if (response.status === 401) {
                // redirect to login
                window.location.replace("/#/login");
            } else if (response.status === 403) {
                alert("No admin rights");
            } else if (response.status === 400) {
                alert("user_limit out of range");
            } else if (response.status === 200) {
                response.json().then((data) => {
                    // using static test data for now as data type is not disccused yet
                    itemsRight = [];
                    let exerciseData = Object.values(data)[0];
                    let exerciseContent =
                        exerciseData["exercise_content"]["list"];
                    for (let i = 0; i < exerciseContent.length; i++) {
                        itemsLeft[i] = { id: i + 1, name: exerciseContent[i] };
                    }
                    itemsLeftOriginal = itemsLeft.slice();
                    exerciseTitle = exerciseData["exercise_title"];
                    exerciseDescription = exerciseData["exercise_description"];
                    exerciseID = exerciseData["exercise_id"];
                });
            }
        });
    };

    function reset() {
        itemsLeft = itemsLeftOriginal.slice();
        itemsRight = [];
    }

    function testGetExercise() {
        // TODO get blankPositions from server
        blankPositions = [18, 68, 89, 132, 263];
        let blankNum = blankPositions.length;

        // Prepare entries with empty string
        userEntries = Array(blankNum).fill("");

        // TODO get the text from the server
        let text =
            "Lorem ipsum dolor  amet, consectetur adipiscing elit. Aliquam magna , pretium ut nibh a,  porttitor nisl. Pellentesque ornare, odio  suscipit eleifend, elit nibh fermentum. Sed auctor sollicitudin dolor, ut tincidunt diam elementum non. Phasellus ut velit at sem  porttitor a eget ante.";
        textPieces = Array(2 * blankNum + 1).fill("");

        
        for (let i=0; i<blankNum + 1; i++) {
            textPieces[2 * i] = text.slice(i==0 ? 0 : blankPositions[i-1],  blankPositions[i]);
            if (i != blankNum) {
                textPieces[2 * i + 1] = "_";
            }
        }
        console.log(text);
        console.log(blankNum);
        console.log(textPieces);
    }
    testGetExercise();
    // getExercise();
    // Assumptions for the format of the text and blank posisions:
    // - text as plain one line string
    // - blanks are just insertet into text without modifying the text -> all spaces surounding the blanks have to be there
    // - blanks are just within the text eg 5 blanks -> 6 textpieces 
</script>

<Page
    title="Fill in the Blanks Exercise"
    fullwidth={true}
    requiredAccessLevel={accessLevels.undefined}
>
<!-- TODO change requiredAccessLevel to accessLevels.user -->
    <div class="exercise-container">
        <div class="header-area">
            <h3>{exerciseTitle}</h3>
        </div>
        <div class="task-area">
            <TaskCard />
        </div>
        <div class="blanks-area">
            <BlanksCard bind:blankPositions bind:textPieces bind:userEntries />
        </div>
        <StatusBar {reset} {submitSolution} />
    </div>
</Page>

<style lang="scss">
    @use "../variables" as vars;

    .exercise-container {
        display: grid;
        grid-template-columns: 3fr 9fr;
        grid-template-rows: 1.5fr 8fr 0.5fr;
        grid-template-areas:
            "head head"
            "task puzzle"
            "status status";
        gap: 1%;
        padding: 1rem 1rem 0.5rem 1rem;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background-color: black;
    }

    .header-area {
        grid-area: head;
        h3 {
            color: vars.$primaryDark;
        }
    }
    .task-area {
        grid-area: task;
        overflow: auto;
    }
    .blanks-area {
        grid-area: blanks;
        display: flex;
        overflow: hidden;
    }
</style>
