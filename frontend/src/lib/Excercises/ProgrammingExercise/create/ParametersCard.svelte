<script lang="ts">
  import type { UICardActionInterface } from "../../../Common/types";
  import UiCard from "../../../Common/UICard.svelte";
  import ParameterDialog from "./ParameterDialog.svelte";

  let parametersActions: Array<UICardActionInterface> = [
    {
      icon: "add_circle_outline",
      func: openAddParameter,
    },
  ];

  let addParameterDialog = true;
  let parameterType = "number";
  let parameterLabel = "";
  let parameters = [];

  function openAddParameter() {
    addParameterDialog = true;
  }

  function addParameter() {
    parameters = [
      ...parameters,
      {
        label: parameterLabel,
        type: parameterType,
      },
    ];
    addParameterDialog = false;
  }
</script>

<UiCard icon="settings" title="Parameters" actions={parametersActions}>
  {#each parameters as parameter}
    {`${parameter.label}: ${parameter.type}`}
    <br />
  {/each}
</UiCard>

<ParameterDialog
  bind:open={addParameterDialog}
  bind:label={parameterLabel}
  bind:selectedType={parameterType}
  func={addParameter}
/>
