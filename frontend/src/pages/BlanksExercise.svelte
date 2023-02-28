<script lang="ts">
    import Page from "../lib/common/Page.svelte";
    import BlanksCard from "../lib//Excercises/FillInBlanks/BlanksCard.svelte";
    import TaskCard from "../lib/Excercises/TaskCard.svelte";
    import StatusBar from "../lib/Excercises/StatusBar.svelte";
    import { accessLevels } from "../lib/constants";
    import type { FillInBlanksExerciseType } from "../lib/Excercises/exercise";
    import {
        SolutionPostFillInBlanks,
        submitSolution,
        getCurrentTimestamp,
    } from "../lib/Excercises/solution";


    let elapsedTime = 0;
    let solution: SolutionPostFillInBlanks;

    // export let exerciseData: FillInBlanksExerciseType;
    let exerciseData = {
        exercise_id: 0,
        exercise_title: "Exercise",
        exercise_content: {
            text: "Lorem ipsum dolor  amet, consectetur adipiscing elit. Aliquam magna , pretium ut nibh a,  porttitor nisl. Pellentesque ornare, odio  suscipit eleifend, elit nibh fermentum. Sed auctor sollicitudin dolor, ut tincidunt diam elementum non. Phasellus ut velit at sem  porttitor a eget ante.",
            blankPos: [18, 68, 89, 132, 263],
        },
    };
    let blankPositions = exerciseData.exercise_content.blankPos;
    let text = exerciseData.exercise_content.text;

    let userEntries = [];
    let textPieces = [];
    
    function submit() {
        console.log(userEntries);
        solution = {
          solution_exercise: exerciseData.exercise_id,
          solution_date: getCurrentTimestamp(),
          solution_duration: elapsedTime,
          solution_content: {
            list: userEntries,
          }
        }
        submitSolution(solution);
    }

    function reset() {
        prepareGapText();
    }

    function prepareGapText() {
        let blankNum = blankPositions.length;

        // Prepare entries with empty string
        userEntries = Array(blankNum).fill("");
        textPieces = Array(2 * blankNum + 1).fill("");

        for (let i = 0; i < blankNum + 1; i++) {
            textPieces[2 * i] = text.slice(
                i == 0 ? 0 : blankPositions[i - 1],
                blankPositions[i]
            );
            if (i != blankNum) {
                textPieces[2 * i + 1] = "_";
            }
        }
        // console.log(text);
        // console.log(blankNum);
        // console.log(textPieces);
    }
    prepareGapText();

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
            <h3>{exerciseData.exercise_title}</h3>
        </div>
        <div class="task-area">
            <TaskCard />
        </div>
        <div class="blanks-area">
            <BlanksCard bind:textPieces bind:userEntries />
        </div>
        <StatusBar {reset} {submit} bind:elapsedTime />
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
            "task blanks"
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
    }
    .blanks-area {
        grid-area: blanks;
        display: flex;
    }
</style>
