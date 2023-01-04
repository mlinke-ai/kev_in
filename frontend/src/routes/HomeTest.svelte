<script>
  import Button, { Label } from "@smui/button";
  import { PythonSvg, JavaSvg } from "../lib/components/AnimatedSVG/";
  import Page from "../lib/components/common/Page.svelte";
  import LanguageCard from "../lib/components/common/LanguageCard.svelte";
  import { blur } from "svelte/transition";
    import LogoSvg from "../lib/components/AnimatedSVG/LogoSVG.svelte";
</script>

<Page title="Home">
  <header>
    <h3 class="headline">Your best choice to learn how to code.</h3>
    <hr />
    <h5 class="headline">
      Exercises designed by experts with practical experience. Join our
      community today!
    </h5>

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
      <div in:blur={{ delay: 500, duration: 500 }}>
        <LanguageCard
          title="Java."
          description="Oracle Java is the #1 programming language and development
      platform."
        >
          <JavaSvg delayAnimation={750} />
        </LanguageCard>
      </div>
    </div>
  </main>
</Page>

<style lang="scss">
  .headline {
    text-align: center;
  }
  .language-cards-area {
    display: grid;
    margin-top: 5%;
    grid-template-columns: repeat(auto-fit, minmax(400px, 400px));
    align-items: center;
    justify-content: center;
    gap: 100px;
  }

  hr {
    width: 50%;
  }
</style>
