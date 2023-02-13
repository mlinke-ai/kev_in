<script>
  import Button from "@smui/button";

  var open;
  const cookiesAccepted = localStorage.getItem('cookiesAccepted');
  if (cookiesAccepted == "true") {
    open = false;
  } else {
    open = true;
  }

  function okClicked(){
    open = false;
    localStorage.setItem('cookiesAccepted', 'true');
  }
</script>

{#if open}
  <div id="blur" />
  <div id="banner">
        <div id="message">
          <p>
            This website uses cookies to provide all functionalities.
            <br />
            By using this site you consent to these cookies!
          </p>
        </div>
      <Button id="button" slot="actions" on:click={() => okClicked()}
        >Okay</Button
      >
  </div>
{/if}

<style>
  #blur {
    position: fixed;
    top: 0vh;
    left: 0vw;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(5px);
    z-index: 1000;
  }

  #banner {
    position: fixed;
    top: 40vh;
    left: 33vw;

    width: 32vw;
    height: fit-content;

    padding-left: 1vw;
    padding-right: 1vw;
    padding-bottom: 2vh;
    padding-top: 2vh;
    text-align: center;

    background-color: rgba(0,57,49,1);
    border-radius: 2vw;
    z-index: 1001;
  }

  #message {
    text-align: center;
    font-size: larger;
  }

  * :global(#button) {
    color: white;
    background-color: #005f50;
  }
</style>
