<script lang="js">
  import Button from "@smui/button";
  import { blur } from "svelte/transition";

  function toTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }
</script>

<!--
  The Footer is a component. Just put it on the bottom of you html body.
  It contains:
  - copyright information
  - link to imprint and dsgvo
  - link to github page
  - button to scroll back to top
 -->

<footer class="bottom-footer" in:blur={{ duration: 2000 }}>
  <Button class="footer-btn">
    Copyright © 2007 Free Software Foundation, Inc.
  </Button>
  <Button class="footer-btn">imprint & dsgvo</Button>

  <Button
    class="footer-btn"
    on:click={() => window.open("https://github.com/mlinke-ai/kev.in")}
    >github</Button
  >
  <Button class="footer-btn" on:click={() => toTop()}>scroll back to top</Button
  >
</footer>

<style>
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

    /* use fixed position so that it sticks to the bottom of the screen*/
    /* position: fixed;*/
    bottom: 0;
  }
</style>
