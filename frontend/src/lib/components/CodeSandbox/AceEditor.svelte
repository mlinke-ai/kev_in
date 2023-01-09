<script>
    import Button, { Icon, Label } from "@smui/button";
    import Card from "@smui/card";
    import Select, { Option } from "@smui/select";
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

<div class="editor-container">
    <Card class="editor-card">
        <div class="editor-header">
            <div class="editor-title">
                <Icon class="material-icons">code</Icon>
                <b>Coding</b>
            </div>
            <div class="action-buttons">
                <Select class="shaped-filled" variant="filled" bind:value label="Language">
                    <Option value="ace/mode/python">Python</Option>
                    <Option value="ace/mode/java">Java</Option>
                </Select>
                <Button class="md-button">
                    <Icon class="material-icons">restart_alt</Icon>
                    <Label>Reset</Label>
                </Button>
                <Button class="md-button">
                    <Icon class="material-icons">play_circle</Icon>
                    <Label>Run</Label>
                </Button>
            </div>
        </div>
        <div class="coding-area">
            <div id="javascript-editor" />
        </div>
    </Card>
</div>

<style lang="scss">
    * {
        box-sizing: border-box;
    }
    * :global(.editor-action-buttons) {
        color: #005f50;
    }
    .editor-container {
        width: 100%;
        height: 100%;
    }
    * :global(.editor-card) {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        border-radius: 1rem 1rem 0.5rem 0.5rem;
    }
    * :global(.editor-card):focus-within {
        filter: drop-shadow(0px 0px 5px #005f50);
    }
    .editor-header {
        padding: 0.7rem 1rem 0.7rem 1rem;
        display: flex;
        align-items: center;
        :last-child {
            margin-left: auto;
        }
    }
    .editor-title {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    .coding-area {
        height: 53vh;
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
