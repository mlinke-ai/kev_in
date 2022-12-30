<script>
    import Page from "../lib/components/Page.svelte";
    import { accessLevels } from "../lib/types";

    const requiredAccessLevel = accessLevels.default
</script>

<Page title="<Page Title>" {requiredAccessLevel}>
    <!-- Your content here, no body tag required --> 
</Page>