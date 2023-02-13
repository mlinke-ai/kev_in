<script>
  import HorizontalList from "./horizontalList.svelte";
  import UiCard from "../../common/UICard.svelte";

  let initHeight = 0;

  export let itemsLeft;
  export let itemsRight;
  let myTestVAR;
  console.log(myTestVAR)
</script>


<UiCard icon="extension" title="Puzzle">
  <div class="lists-container" bind:clientHeight={myTestVAR}>
    <div class="list">
      <HorizontalList bind:items={itemsLeft} height={((myTestVAR)-(myTestVAR)*0.125).toString()}/>
    </div>
    <div class="list">
      <HorizontalList bind:items={itemsRight} height={((myTestVAR)-(myTestVAR)*0.125).toString()}/>
    </div>
  </div>
</UiCard>

<style>
  .lists-container{
    margin: 1rem;
    display: flex;
    flex-direction: row;
    justify-content: center;
    height: 100%;
  }
  .list{
    flex: 1;
  }

</style>