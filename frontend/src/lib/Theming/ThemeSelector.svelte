<script lang="ts">
    import Button from "@smui/button";
import { themes, setTheme } from "./themes"

    
</script>

<Button on:click={() => setTheme(themes[1], true)}>Set Theme</Button>
<Button on:click={() => setTheme(themes[0], true)}>Reset Theme</Button>