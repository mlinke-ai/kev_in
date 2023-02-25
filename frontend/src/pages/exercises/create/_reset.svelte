<script>
    import { redirect } from "@roxi/routify";
    import { accessLevels } from "../../../lib/Common/types";
    import { accessLevel, startPage } from "../../../stores";
  /*
    if ($accessLevel < accessLevels.admin) {
      $redirect($startPage);
    }
    */
  </script>
  
  <!--{#if $accessLevel >= accessLevels.admin}
    
  {/if}-->
  <slot />