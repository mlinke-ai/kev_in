<script lang="ts">
  import Button, { Icon, Label } from "@smui/button";
  import { Actions, Content, Title } from "@smui/dialog";
  import Dialog from "@smui/dialog/src/Dialog.svelte";
  import Textfield from "@smui/textfield";
  import HelperText from "@smui/textfield/helper-text";

  export let open;
  export let edit = false;
  export let input;
  export let output;
  export let index = 0;
  export let func;

  let dialogTitle = "Add Test Case";
  let buttonLabel = "Add";
  let buttonIcon = "add";

  if (edit) {
    dialogTitle = `Edit Test Case #${index + 1}`;
    buttonLabel = "Edit";
    buttonIcon = "edit";
  }
</script>

<Dialog bind:open class="dialog">
  <Title>{dialogTitle}</Title>
  <Content>
    <div class="add-test-case-content">
      <div class="add-test-case-input">
        <Textfield label="Input" bind:value={input}>
          <HelperText slot="helper">Comma-seperated list of inputs</HelperText>
        </Textfield>
      </div>
      <div class="add-test-case-output">
        <Textfield label="Expected Output" bind:value={output}>
          <HelperText slot="helper">Comma-seperated list of outputs</HelperText>
        </Textfield>
      </div>
    </div>
  </Content>
  <Button color="secondary" on:click={func}>
    <Label>{buttonLabel}</Label>
    <Icon class="material-icons">{buttonIcon}</Icon>
  </Button>
</Dialog>

<style lang="scss">
  .add-test-case-content {
    display: flex;
    gap: 1rem;
  }
</style>
