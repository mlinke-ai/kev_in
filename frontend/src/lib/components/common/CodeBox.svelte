<script>
  import Button from "@smui/button";
  import Select, { Option } from "@smui/select";
  import AceEditor from "../AceEditor/AceEditor.svelte";
  import "brace/mode/python";
  import "brace/theme/twilight";
  let text = "";
  let themes = ["dracula", "github"];
  let selectedTheme = "dracula";
  let languages = ["python", "java"];
  let selectedLanguage = "python";
</script>

<div class="codebox">
  <div class="coding-area">
    <AceEditor />
  </div>
</div>

<style lang="scss">
  * {
        box-sizing: border-box;
    }
  .codebox {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    justify-items: stretch;
  }
  .coding-area {
    position: relative;
  }
  #editor {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
}
</style>
