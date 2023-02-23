<script>
  import { onMount } from "svelte";
  import Page from "../lib/common/Page.svelte";
  import { accessLevels } from "../lib/common/types";

  const requiredAccessLevel = accessLevels.user
  let ready = false;

  onMount(() => {
    ready = true;
  });
</script>

<Page {requiredAccessLevel}>
  Hello!
</Page>
