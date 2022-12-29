<script>
  import Button, { Label } from "@smui/button";
  import { PythonSvg, JavaSvg } from "../lib/components/AnimatedSVG/";
  import Page from "../lib/components/Page.svelte";
  import LanguageCard from "../lib/components/LanguageCard.svelte";
  import { blur } from "svelte/transition";
</script>

<Page title="Home">
  <header>
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
  </header>
  <main>
    <div class="language-cards-area">
      <div in:blur={{ duration: 500 }}>
        <LanguageCard
          title="Python."
          description="Worldwide beloved and broadly used high-level programming
    language."
        >
          <PythonSvg />
        </LanguageCard>
      </div>
      <div in:blur={{ delay:500, duration: 500 }}>
        <LanguageCard
          title="Java."
          description="Oracle Java is the #1 programming language and development
      platform."
        >
          <JavaSvg delayAnimation={750}/>
        </LanguageCard>
      </div>
    </div>
  </main>
</Page>

<style global>
  .headline {
    text-align: center;
  }
  .language-cards-area {
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
