<!-- <script>
    import Page from "../lib/common/Page.svelte";
    import Button from "@smui/button";

    // `Lorem ipsum dolor <input type="text"> amet, consectetur adipiscing elit.
    // Aliquam magna <input type="text">, pretium ut nibh a, <input type="text"> porttitor nisl.
    // Pellentesque ornare, odio <input type="text"> suscipit eleifend, elit nibh fermentum.
    // Sed auctor sollicitudin dolor, ut tincidunt diam elementum non.
    // Phasellus ut velit at sem <input type="text"> porttitor a eget ante.`

    // `Lorem ipsum dolor  amet, consectetur adipiscing elit.
    // Aliquam magna , pretium ut nibh a,  porttitor nisl.
    // Pellentesque ornare, odio  suscipit eleifend, elit nibh fermentum.
    // Sed auctor sollicitudin dolor, ut tincidunt diam elementum non.
    // Phasellus ut velit at sem  porttitor a eget ante.`

    `
    - neue struktur mit forEach
    - page -> BlanksCard -> UICard
    - smui textfield
    `


    var entries = [];
    var text = "";
    var blankPositions = [];
    const inputIdPrefix = "blankNr";

    function loadText() {
        // TODO get blankPositions from server
        blankPositions = [18, 68, 89, 132, 263];

        // Sort blankPosisions and reverse to make inserting into the text more easy
        blankPositions.sort((a, b) => a - b);
        blankPositions.reverse();

        // Prepare entries with empty string
        entries = Array(blankPositions.length).fill("");

        // TODO get the text from the server
        text =
            "Lorem ipsum dolor  amet, consectetur adipiscing elit. Aliquam magna , pretium ut nibh a,  porttitor nisl. Pellentesque ornare, odio  suscipit eleifend, elit nibh fermentum. Sed auctor sollicitudin dolor, ut tincidunt diam elementum non. Phasellus ut velit at sem  porttitor a eget ante.";

        // Insert blankHtml on desired positions in text
        // blankPositions.forEach(pos =>
        // {text = text.slice(0, pos) + '<input type="text" bind:value={entries}>' + text.slice(pos);});
        for (let i = 0; i < blankPositions.length; i++) {
            text =
                text.slice(0, blankPositions[i]) +
                '<input type="text" id="' +
                inputIdPrefix +
                i +
                '">' +
                text.slice(blankPositions[i]);
        }
    }

    loadText();
</script>

<Page>
    <h1>Fill in the Blanks</h1>

    <p>{@html text}</p>


    <Button class="submit-btn" on:click={() => {
        console.log(text);
        for (let i=0; i<entries.length; i++) {
            entries[i] = document.getElementById(inputIdPrefix + i).value;
        }
        console.log(entries);
    }}
        >submit</Button
    >
</Page> -->
