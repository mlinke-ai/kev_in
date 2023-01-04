<script>
  import Button from "@smui/button";
  import Select, { Option } from "@smui/select";
  import { AceEditor } from "svelte-ace";
  import "brace/mode/python";
  import "brace/theme/twilight";
  let text = "";
  let themes = ["dracula", "github"];
  let selectedTheme = "dracula";
  let languages = ["python", "java"];
  let selectedLanguage = "python";
</script>

<div class="codebox">
  <div class="codebox-header">
    <div class="codebox-title">Example task</div>
    <div class="codebox-settings-area">
      <Select
        class="shaped-filled"
        variant="filled"
        bind:selectedLanguage
        label="Language"
      >
        {#each languages as language}
          <Option value={language}>{language}</Option>
        {/each}
      </Select>
      <Select
        class="shaped-filled"
        variant="filled"
        bind:selectedTheme
        label="Theme"
      >
        {#each themes as theme}
          <Option value={theme}>{theme}</Option>
        {/each}
      </Select>
    </div>
  </div>
  <div class="coding-area">
    <AceEditor
      width="100%"
      height="400px"
      lang={selectedLanguage}
      theme="twilight"
      value={text}
      options={{fontSize: 30}}
    />
    <Button>Compile</Button>
  </div>
</div>

<style lang="scss">
  .codebox {
    width: 80%;
    box-sizing: border-box;
    bottom: 0;
    position: absolute;
  }
  .codebox-header {
    display: flex;
    padding: 0 1rem 0 1rem;
    align-items: center;
    :last-child {
      margin-left: auto;
    }
  }
</style>
