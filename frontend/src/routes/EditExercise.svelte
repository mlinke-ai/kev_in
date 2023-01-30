<script>
    import Page from "../lib/components/common/Page.svelte";
    import Tab, { Label } from "@smui/tab";
    import TabBar from "@smui/tab-bar";
    import Textfield from "@smui/textfield";
    import HelperText from "@smui/textfield/helper-text";
    import Button from "@smui/button";

    let active = "Sandbox";

    let title = "";
    let description = "";
    let functionSignature = "";
    let test = "";
</script>

<Page>
    <div>
        <!--
          Note: tabs must be unique. (They cannot === each other.)
        -->
        <TabBar
            tabs={["Sandbox", "Parsons Puzzle", "Gap Text"]}
            let:tab
            bind:active
        >
            <!-- Note: the `tab` property is required! -->
            <Tab {tab}>
                <Label>{tab}</Label>
            </Tab>
        </TabBar>

        <div>
            {#if active == "Sandbox"}
                <div class="forms">
                    <Textfield
                        bind:value={title}
                        variant="outlined"
                        helperLine$style="width: 100%;"
                        class="textfields"
                    >
                        <HelperText persistent slot="helper">Title</HelperText>
                    </Textfield>

                    <Textfield
                        bind:value={description}
                        variant="outlined"
                        textarea
                        helperLine$style="width: 100%;"
                        class="textfields"
                    >
                        <HelperText persistent slot="helper"
                            >Description</HelperText
                        >
                    </Textfield>

                    <Textfield
                        bind:value={functionSignature}
                        variant="outlined"
                        helperLine$style="width: 100%;"
                        class="textfields"
                    >
                        <HelperText persistent slot="helper">Function Signature</HelperText>
                    </Textfield>

                    <Textfield
                    bind:value={test}
                    variant="outlined"
                    textarea
                    helperLine$style="width: 100%;"
                    class="textfields"
                >
                    <HelperText persistent slot="helper"
                        >Test</HelperText
                    >
                </Textfield>

                <Button on:click={()=>true} variant="raised" style="margin-top: 3em;">
                    <Label>Submit</Label>
                  </Button>
                </div>
            {:else if active == "Parsons Puzzle"}
                <h1>PARSONS PUZZLE</h1>
            {:else}
                <h1>GAP TEXT</h1>
            {/if}
        </div>
    </div>
</Page>

<style>
    * :global(.textfields)  {
        margin-top: 2em;
        width: 100%;
    }
</style>
