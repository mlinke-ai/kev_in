<script>
    import Page from "../lib/components/common/Page.svelte";
    import { AceEditor } from "svelte-ace";
    import "brace/mode/python";
    import "brace/theme/dracula";
    import "brace/theme/github";
    import Card from "@smui/card";
    import Button from "@smui/button";
    import Select, { Option } from "@smui/select";
    let text = "";
    let themes = ["dracula", "github"];
    let selectedTheme = "dracula";
    let languages = ["python", "java"]
    let selectedLanguage = "python";
</script>

<Page title="Coding Sandbox" fullwidth={true}>
    <Card class="coding-area">
        <Select class="shaped-filled" variant="filled" bind:selectedLanguage label="Language">
            {#each languages as language}
                <Option value={language}>{language}</Option>
            {/each}
        </Select>
        <Select class="shaped-filled" variant="filled" bind:selectedTheme label="Theme">
            {#each themes as theme}
                <Option value={theme}>{theme}</Option>
            {/each}
        </Select>
        <AceEditor
            width="100%"
            height="100px"
            lang={selectedLanguage}
            theme="dracula"
            value={text}
        />
        <Button>Compile</Button>
    </Card>
</Page>
