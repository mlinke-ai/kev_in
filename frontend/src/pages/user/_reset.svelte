<script>
  import { redirect } from "@roxi/routify";
  import { accessLevels } from "../../lib/Common/types";
  import Navbar from "../../lib/Navbar/Navbar.svelte";
  import { accessLevel, startPage } from "../../stores";

  if ($accessLevel < accessLevels.user) {
    $redirect($startPage)
  }
</script>

{#if $accessLevel >= accessLevels.user}
  <Navbar />
  <slot />
{/if}
