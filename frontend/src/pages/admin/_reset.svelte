<script>
  import { redirect } from "@roxi/routify";
  import { accessLevels } from "../../lib/Common/types";
  import Navbar from "../../lib/Navbar/Navbar.svelte";
  import { accessLevel, startPage } from "../../stores";

  if ($accessLevel < accessLevels.admin) {
    $redirect($startPage)
  }
</script>

{#if $accessLevel >= accessLevels.admin}
  <Navbar />
  <slot />
{/if}
