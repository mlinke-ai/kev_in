<script lang="js">
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

<footer class="bottom-footer">
    <Button class="footer-btn">
      Copyright © 2007 Free Software Foundation, Inc.
    </Button>

    <Button class="footer-btn">impressum & dsgvo</Button>

    <Button
      class="footer-btn"
      on:click={() => window.open("https://github.com/mlinke-ai/kev.in")}
      >github</Button
    >

    <Button class="footer-btn" on:click={() => toTop()}
      >zurück nach oben</Button
    >
</footer>

<style>
  body {
    margin: 0;
    padding: 0;
  }
  * :global(.footer-btn) {
    color: white;
  }
  .bottom-footer {
    align-items: center;
    background-color: rgba(0, 0, 0, 0.2);
    display: flex;
    justify-content: space-between;
    padding-left: 8rem;
    padding-right: 8rem;
    box-sizing: border-box;
    width: 100%;
    height: 50px;
    border-radius: 8rem;
  }
</style>
