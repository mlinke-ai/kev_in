<script lang="ts">
  import Snackbar, { Label, Actions } from "@smui/snackbar";
  import IconButton from "@smui/icon-button";
  import { messages } from "../../constants";
  import { onMount } from "svelte";

  export let message;
  export let type: messages = messages.neutral;
  export let content = "";
  export let autoOpen = false;

  let messageClass;

  switch (type) {
    case messages.neutral:
      messageClass = "message-neutral";
      break;
    case messages.success:
      messageClass = "message-success";
      break;
    case messages.warning:
      messageClass = "message-warning";
      break;
    case messages.error:
      messageClass = "message-error";
      break;
  }

  if (autoOpen) {
    onMount(() => {
      message.open();
    });
  }
</script>

<Snackbar bind:this={message} class={messageClass}>
  <Label>{content}</Label>
  <Actions>
    <IconButton class="material-icons" title="Dismiss">close</IconButton>
  </Actions>
</Snackbar>
