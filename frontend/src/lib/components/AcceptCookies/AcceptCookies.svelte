<script>
  import Button from "@smui/button";
  import Banner, { Label } from "@smui/banner";

  let open = true;
</script>

{#if open}
  <div id="blur" />
  <div id="banner">
    <Banner
      id="banner"
      open
      fixed
      mobileStacked
      content$style="max-width: max-content;"
    >
      <Label slot="label">
        <div id="message">
          <p>
            This website uses cookies to provide all functionalities.
            <br />
            By using this site you consent to these cookies!
          </p>
        </div>
      </Label>
      <Button id="button" slot="actions" on:click={() => (open = false)}
        >Okay</Button
      >
    </Banner>
  </div>
{/if}

<style>
  #blur {
    position: fixed;
    top: 0%;
    left: 0%;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(5px);
  }

  #banner {
    position: fixed;
    top: 50%;
    left: 50%;

    width: 420px;
    height: 120px;
    margin-top: -60px;
    margin-left: -210px;

    background-color: rgba(0, 20, 17, 1);
    border-radius: 20px;
  }

  #message {
    padding-left: 15px;
  }

  * :global(#button) {
    left: 65%;
    color: white;
    background-color: rgba(0, 57, 49, 1);
  }
</style>
