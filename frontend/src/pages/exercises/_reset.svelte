<script>
  import { redirect } from "@roxi/routify";
  import { accessLevels } from "../../lib/Common/types";
  import { accessLevel, startPage } from "../../stores";

  if ($accessLevel < accessLevels.user) {
    $redirect($startPage);
  }
</script>

{#if $accessLevel >= accessLevels.user}
  <slot />
{/if}
