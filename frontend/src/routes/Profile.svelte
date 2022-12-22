<script>
    import { blur } from "svelte/transition";
    import Page from "../lib/components/Page.svelte";
</script>

<Page title="Profile">
    <p in:blur="{{ duration: 2000 }}">Logged In!</p>
</Page>