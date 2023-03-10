<script lang="ts">
  import Profile from "../../user/profile.svelte";
  
    export let userID: any;
    userID = userID as unknown as number;
  
  </script>
  
  <Profile {userID}/>