<script>
    import Page from "../lib/common/Page.svelte";
    import { accessLevels } from "../lib/common/types";

    const requiredAccessLevel = accessLevels.default
</script>

<Page title="<Page Title>" {requiredAccessLevel}>
    <!-- Your content here, no body tag required --> 
</Page>