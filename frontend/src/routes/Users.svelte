<script>
  import Button from "@smui/button/src/Button.svelte";
  import Page from "../lib/components/common/Page.svelte";
</script>

<Page>
  <h1>Users</h1>

  <p>This is a placeholder site for listing all users.</p>

  <p />

  <div class="grid-container">
    <div class="grid-item">User 1</div>
    <div class="grid-item">User 2</div>
    <div class="grid-item">User 3</div>
    <div class="grid-item">User 4</div>
    <div class="grid-item">User 5</div>
    <div class="grid-item">User 6</div>
    <div class="grid-item">User 7</div>
    <div class="grid-item">User 8</div>
    <div class="grid-item">User 9</div>
    <div class="grid-item">User 10</div>
    <div class="grid-item">User 11</div>
    <div class="grid-item">User 12</div>
    <div class="grid-item">User 13</div>
    <div class="grid-item">User 14</div>
    <div class="grid-item">User 15</div>
  </div>

  <a href="/#/admin-dashboard">
    <Button>Back to dashboard</Button>
  </a>
</Page>

<style>
  .grid-container {
    display: grid;
    grid-template-columns: auto auto auto;
    background-color: rgb(0, 57, 49);
    padding: 10px;
  }
  .grid-item {
    background-color: #001a16;
    border: 1px solid rgba(0, 0, 0, 0.8);
    padding: 20px;
    font-size: 30px;
    text-align: center;
  }
</style>
