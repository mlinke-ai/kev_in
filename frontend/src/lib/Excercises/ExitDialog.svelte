<script lang="ts">
  import Dialog, { Title, Content, Actions } from '@smui/dialog';
  import Button, { Label } from '@smui/button';
  import { getStartPage } from '../Authentication/user';
  import { redirect } from '@roxi/routify';
  import { startPage } from "../../stores";
  import AcceptCookies from '../AcceptCookies/AcceptCookies.svelte';

  export let open = false;
</script>

<Dialog
  bind:open
  aria-labelledby="simple-title"
  aria-describedby="simple-content"
>
  <!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
  <Content id="simple-content">
    Are you sure that you want to exit?<br/>
    Unsaved progress will not be saved.
  </Content>
  <Actions>
    <Button variant="raised">
      <Label>No</Label>
    </Button>
    <Button variant="outlined" on:click={() => window.history.back()}>
      <Label>Yes</Label>
    </Button>
  </Actions>
</Dialog>
 