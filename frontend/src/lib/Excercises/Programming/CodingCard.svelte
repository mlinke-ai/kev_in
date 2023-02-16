<!-- Component that provides an editor with syntax highlighting for
     Java and Python using ace -->
<script lang="ts">
  import UiCard from "../../common/UICard.svelte";
  import * as ace from "brace";
  import "brace/mode/python";
  import "brace/mode/java";
  import "brace/theme/gob";
  import { onMount } from "svelte";
  import { languages } from "../../constants";

  let editor;
  let modes = ["ace/mode/python", "ace/mode/java"];
  let ready = false;

  export let content = "";
  export let language: languages = languages[0];

  // quick fix till backend sends numeric data instead of strings
  let mode_index = 0;
  if (language == "Java") {
    mode_index = 1;
  }
  onMount(() => {
    editor = ace.edit("editor");
    editor.getSession().setMode(modes[mode_index]);
    editor.setTheme("ace/theme/gob");
    editor.setValue(content, 1);
    editor.setOptions({
      showPrintMargin: false,
      fontSize: 18,
      fontFamily: "Roboto Mono",
    });
    editor.session.on('change', () => {content = editor.getValue()});

});
</script>

<UiCard icon="code" title="Coding">
  <div class="coding-area">
    <div id="editor" />
  </div>
</UiCard>

<style lang="scss">
  .coding-area {
    height: 55vh;
    width: 100%;
    position: relative;
    overflow: scroll;
  }
  #editor {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: 0 0.5rem 0.5rem 0.5rem;
    border-radius: 0.5rem;
  }
</style>
