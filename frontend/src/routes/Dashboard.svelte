<script>
  import { onMount } from "svelte";
  import Page from "../lib/components/common/Page.svelte";
  import { accessLevels } from "../lib/constants";

  const requiredAccessLevel = accessLevels.user
  let ready = false;

  onMount(() => {
    ready = true;
  });
</script>

<Page {requiredAccessLevel}>
  Hello!
</Page>
