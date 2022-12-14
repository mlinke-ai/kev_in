<script lang="js">
  import BottomAppBar, { Section } from "@smui-extra/bottom-app-bar";
  import Button from "@smui/button";

  function toTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }
</script>

<!-- 
  The Footer is a component. Just put it on the bottom of you html body.
  It contains:
  - copyright information
  - link to impressum and dsgvo
  - link to github page
  - button to scroll back to top
 -->

<div class="bottom-footer">
  <BottomAppBar variant="static">
    <Section>
      <Button class="footer-btn">
        Copyright © 2007 Free Software Foundation, Inc.
      </Button>
    </Section>

    <Section>
      <Button class="footer-btn">impressum & dsgvo</Button>
    </Section>

    <Section>
      <Button
        class="footer-btn"
        on:click={() => window.open("https://github.com/mlinke-ai/kev.in")}
        >github</Button
      >
    </Section>

    <Section>
      <Button class="footer-btn" on:click={() => toTop()}
        >zurück nach oben</Button
      >
    </Section>
  </BottomAppBar>
</div>

<style>
  * :global(.footer-btn) {
    color: white;
  }
  .bottom-footer {
    width: 100%;
    height: 50px;
  }
</style>
