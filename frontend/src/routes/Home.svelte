<script>
  import Button, { Label } from "@smui/button";
  import { PythonSvg, JavaSvg } from "../lib/components/AnimatedSVG";
  import Page from "../lib/components/common/Page.svelte";
  import LanguageCard from "../lib/components/common/LanguageCard.svelte";
  import { blur } from "svelte/transition";
  import AuthDialog from "../lib/components/Authentication/AuthDialog.svelte";
  import Dialog, { Title, Content, Actions, InitialFocus } from "@smui/dialog";
  import Footer from "../lib/components/Footer/Footer.svelte";

  let open = false;
</script>

<Page title="Home">
  <header>
    <h3>Your best choice to learn how to code.</h3>
    <hr />
    <h5>
      Exercises designed by experts with practical experience. Join our
      community today!
    </h5>
    <Button
      variant="raised"
      color="primary"
      on:click={() => {
        open = true;
      }}
    >
      <Label>Start now</Label>
    </Button>
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
  <Dialog bind:open>
    <AuthDialog />
  </Dialog>
</Page>
<Footer />

<style lang="scss">
  header {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .language-cards-area {
    display: grid;
    margin-top: 5%;
    justify-content: center;
    grid-template-columns: repeat(auto-fit, minmax(400px, 400px));
    gap: 50px;
  }

  hr {
    width: 50%;
  }
</style>
