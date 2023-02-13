<script>
  import { Content, Media } from "@smui/card";
  import Card from "@smui/card";
  import Button from "@smui/button";
  import { Label } from "@smui/button";
  import Page from "../lib/common/Page.svelte";

  import { startPage } from "../stores";
  import { replace as replaceRoute } from "svelte-spa-router";

  export const params=""

  function goToStartPage(){
    replaceRoute($startPage);
  }
</script>

<Page title="Page not found">
  <h1 class="title">ERROR 404</h1>

  <div class="card-container">
    <Card>
      <div style="padding: 1rem;">
        <h2
          class="mdc-typography--headline6"
          style="margin: 0; font-family: sans-serif;"
        >
          I'm sorry, we couldn't find the page you were looking for :(
        </h2>
      </div>

      <Media class="card-media-16x9" aspectRatio="16x9" />
      <Content class="mdc-typography--body2">
        <p style="left: 40px; font-family: sans-serif;">
          Want to go back to starting page instead?
        </p>

       
        <Button on:click={() => goToStartPage()}
          style="left: 20px; border:solid;">
          <Label>Go back</Label>
        </Button>
      </Content>
    </Card>
  </div>
</Page>

<style>
  .title {
    color: aliceblue;
    font-family: monospace;
  }

  * :global(.card-media-16x9) {
    background-image: url("404-not-found.png");
    background-repeat: no-repeat;
    background-position: center;
  }
</style>
