<script lang="ts">
  import Button, { Icon, Label } from "@smui/button";
  import { Actions, Content, Title } from "@smui/dialog";
  import Dialog from "@smui/dialog/src/Dialog.svelte";
  import Textfield from "@smui/textfield";
  import HelperText from "@smui/textfield/helper-text";
  import Select, { Option } from "@smui/select";

  export let open;
  export let edit = false;
  export let label;
  export let index = 0;
  export let func;

  let dialogTitle = "Add Parameter";
  let buttonLabel = "Add";
  let buttonIcon = "add";

  export let selectedType;
  let types = ["number", "string"];

  if (edit) {
    dialogTitle = `Edit Parameter #${index + 1}`;
    buttonLabel = "Edit";
    buttonIcon = "edit";
  }
</script>

<Dialog bind:open class="dialog">
  <Title>{dialogTitle}</Title>
  <Content>
    <div class="add-parameter-content">
      <div class="add-parameter-type">
        <Select bind:value={selectedType} label="Select Type">
          {#each types as t}
            <Option value={t}>{t}</Option>
          {/each}
        </Select>
      </div>
      <div class="add-parameter-label">
        <Textfield label="Label" bind:value={label}>
          <HelperText slot="helper">Enter label for the parameter</HelperText>
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
