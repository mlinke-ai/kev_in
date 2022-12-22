<script>
  import Button, { Label } from "@smui/button";
  import Card from "@smui/card";
  import { Media } from "@smui/card";
  import JavaSvg from "../lib/components/AnimatedSVG/JavaSVG.svelte";
  import PythonSvg from "../lib/components/AnimatedSVG/PythonSVG.svelte";
  import Page from "../lib/components/Page.svelte";
  import Ripple from "@smui/ripple";
  import { blur } from "svelte/transition";
  import LanguageCard from "../lib/components/LanguageCard.svelte";
</script>

<Page title="Home">
  <div class="home-page">
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
      <LanguageCard
        title="Python."
        description="Worldwide beloved and broadly used high-level programming
      language."
      >
        <PythonSvg />
      </LanguageCard>
      <LanguageCard
        title="Java."
        description="Oracle Java is the #1 programming language and development
        platform."
      >
        <JavaSvg />
      </LanguageCard>
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
  .grid {
    display: flex;
    margin-top: 5%;
    align-items: center;
    justify-content: center;
    gap: 100px;
  }

  hr {
    width: 50%;
  }
</style>
