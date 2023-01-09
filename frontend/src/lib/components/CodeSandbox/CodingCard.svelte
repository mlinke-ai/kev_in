<script>
    import UiCard from "../common/UICard.svelte";
    import * as ace from "brace";
    import "brace/mode/python";
    import "brace/mode/java";
    import "brace/theme/gob";
    import { onMount } from "svelte";

    let editor
    let value = "ace/mode/python"
    let defaultContentPython = "# print Hello World\n\n";
    let defaultContentJava = "// print Hello World\n\n";
    let ready = false

    $: setLanguage(value);

    onMount(() => {
        editor = ace.edit("javascript-editor");
        editor.getSession().setMode("ace/mode/python");
        editor.setTheme("ace/theme/gob");
        editor.setValue(defaultContentPython, 1);
        editor.setOptions({
            showPrintMargin: false,
            fontSize: 18,
            fontFamily: "Roboto Mono",
        });
        ready = true
    });

    function setLanguage(lang) {
        if (ready) {
            editor.getSession().setMode(lang);
            console.log(lang)
        }
    }

    function reset() {}
</script>

<UiCard icon="code" title="Coding">
    <div class="coding-area">
        <div id="javascript-editor" />
    </div>
</UiCard>

<style lang="scss">
    .coding-area {
        height: 55vh;
        width: 100%;
        position: relative;
        overflow: scroll;
    }
    #javascript-editor {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        margin: 0 0.5rem 0.5rem 0.5rem;
        border-radius: 0.5rem;
    }
</style>
