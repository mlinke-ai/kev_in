<script>
  import Button, { Label } from "@smui/button";
  import Card from "@smui/card";
  import { Media } from "@smui/card";
  import Page from "./Page.svelte";
</script>

<Page title="Home">
  <div class="home-page" in:blur={{ duration: 250 }}>
    <h1 class="headline">Your best choice to learn how to code.</h1>
    <hr />
    <h2 class="headline">
      Exercises designed by experts with practical experience. Join our
      community today!
    </h2>

    <div align="center">
      <a href="#/login">
        <Button variant="raised" color="primary">
          <Label>Start now</Label>
        </Button>
      </a>
    </div>

    <div class="grid">
      <div class="language-card">
        <Card style="width: 400px; border-radius:40px">
          <Media class="card-media-square-python" aspectRatio="square">
            <div
              style="color: #fff; position: absolute; bottom: 16px; left: 16px;"
            >
              <h2 class="mdc-typography--headline6" style="margin: 0;">
                Python.
              </h2>
              <h3 class="mdc-typography--subtitle2" style="margin: 0;">
                Worldwide beloved and broadly used high-level programming
                language.
              </h3>
            </div>
          </Media>
        </Card>
      </div>

      <div class="language-card">
        <Card style="width: 400px; border-radius:40px">
          <Media class="card-media-square-java" aspectRatio="square">
            <div
              style="color: #fff; position: absolute; bottom: 16px; left: 16px;"
            >
              <h2 class="mdc-typography--headline6" style="margin: 0;">
                Java.
              </h2>
              <h3 class="mdc-typography--subtitle2" style="margin: 0;">
                Oracle Java is the #1 programming language and development
                platform.
              </h3>
            </div>
          </Media>
        </Card>
      </div>
    </div>
  </div>

  <!-- <div>
    <LayoutGrid>
      {#each Array(2) as _unused, i}
        <Cell align="middle">
          <div class="demo-cell">Cell {i + 1}</div>
        </Cell>
      {/each}
    </LayoutGrid>
    </div> -->
</Page>

<style global>
  .headline {
    text-align: center;
  }
  * :global(.card-media-square-java) {
    background-image: url("./src/assets/java.svg");
    background-size: 70%;
    background-position-y: 20%;
  }
  * :global(.card-media-square-python) {
    background-image: url("./src/assets/python.svg");
    background-size: 110%;
    background-position-y: 70%;
  }
  .grid {
    display: flex;
    margin-top: 5%;
    align-items: center;
    justify-content: center;
    gap: 100px;
  }

  .language-card {
    margin: 5px;
  }

  hr {
    width: 50%;
  }
</style>
