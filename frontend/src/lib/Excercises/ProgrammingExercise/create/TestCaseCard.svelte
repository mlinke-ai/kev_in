<script lang="ts">
  import {
    messages,
    UICardActionInterface,
  } from "../../../../lib/Common/types";
  import UiCard from "../../../../lib/Common/UICard.svelte";

  import Message from "../../../../lib/Common/Message/Message.svelte";
  import Accordion, {
    Panel,
    Header,
    Content as PanelContent,
  } from "@smui-extra/accordion";
  import IconButton from "@smui/icon-button/src/IconButton.svelte";
  import TestCaseDialog from "./TestCaseDialog.svelte";

  import type { TestCase } from "./types"
  import { blur, scale } from "svelte/transition";

  let testCaseActions: Array<UICardActionInterface> = [
    {
      icon: "add_task",
      func: openAddTestCase,
    },
  ];

  export let testCases: Array<TestCase> = [];
  // testCases.push({ input: ["123"], output: "123" });
  let testValue = "";
  let testSolution = "";

  let addDialog: boolean;
  let editDialog: boolean;
  let currentIndex: number;

  let emptyFieldsMessage: Message;
  let testCaseAddedMessage: Message;
  let testCaseMessageContent = "";

  function openAddTestCase() {
    addDialog = true;
  }

  function addTestCase() {
    if (testValue == "" || testSolution == "") {
      emptyFieldsMessage.open();
    } else {
      testCases = [
        ...testCases,
        {
          input: testValue.split(",").map(function(val){return (val as unknown as number);}),
          output: testSolution.split(",").map(function(val){return (val as unknown as number);})
        },
      ];
      testValue = "";
      testSolution = "";
      testCaseMessageContent = `Created Test Case #${testCases.length}`;
      testCaseAddedMessage.open();
      addDialog = false;
    }
  }

  function openEditTestCase(index: number) {
    testValue = testCases[index].input.join(", ");
    testSolution = testCases[index].output.join(", ");
    currentIndex = index;
    editDialog = true;
  }

  function editTestCase() {
    if (testValue == "" || testSolution == "") {
      emptyFieldsMessage.open();
    } else {
      testCases[currentIndex] = {
        input: testValue.split(",").map(function(val){return (val as unknown as number);}),
        output: testSolution.split(",").map(function(val){return (val as unknown as number);})
      };
      testValue = "";
      testSolution = "";
      testCaseMessageContent = `Updated Test Case #${testCases.length}`;
      testCaseAddedMessage.open();
      editDialog = false;
    }
  }

  function deleteTestCase(index: number) {
    testCases = testCases.filter((_, i) => i != index);
  }
</script>

<UiCard icon="fact_check" title="Test Cases" actions={testCaseActions}>
  <div class="test-cases-container">
    <Accordion>
      {#each testCases as testCase, index}
      <div class="transitions" in:scale={{ duration: 250 }} out:blur>
        <Panel variant="outlined" color="primary">
            <Header>
              <div class="panel-header">
                Test Case #{index + 1}
                <div class="panel-header-actions">
                  <IconButton
                    size="mini"
                    class="material-icons"
                    style="color: var(--mdc-theme-secondary);"
                    on:click={() => {
                      openEditTestCase(index);
                    }}>edit</IconButton
                  >
                  <IconButton
                    size="mini"
                    class="material-icons"
                    style="color: var(--mdc-theme-secondary);"
                    on:click={() => {
                      deleteTestCase(index);
                    }}>clear</IconButton
                  >
                </div>
              </div>
            </Header>
            <PanelContent>
              Input: {testCase.input}
              <br />
              Output: {testCase.output}
            </PanelContent>
          </Panel>
      </div>

      {/each}
    </Accordion>
  </div>
</UiCard>

<TestCaseDialog
  bind:open={addDialog}
  bind:input={testValue}
  bind:output={testSolution}
  func={addTestCase}
/>
<TestCaseDialog
  bind:open={editDialog}
  bind:input={testValue}
  bind:output={testSolution}
  func={editTestCase}
  edit={true}
  index={currentIndex}
/>

<Message
  bind:message={emptyFieldsMessage}
  type={messages.warning}
  content={"Please enter all values"}
/>

<Message
  bind:message={testCaseAddedMessage}
  type={messages.success}
  content={testCaseMessageContent}
/>

<style>
  .panel-header-actions {
    display: flex;
    margin-left: auto;
  }
  .panel-header {
    display: flex;
    align-items: center;
  }
  .test-cases-container {
    padding: 0 1rem 0 1rem;
  }
</style>
