<script>
  import HorizontalList from "../horizontalList.svelte";
  import UiCard from "../common/UICard.svelte";

  let initHeight = 0;

  let itemsLeft = [
    {id: 1, name: "print(22 + 66 + sum([1,2,3]))"},
    {id: 2, name: "print(22)\n34"},
    {id: 3, name: "item3"},
    {id: 4, name: "item3"},
    {id: 5, name: "item3"},
    {id: 6, name: "item3"},
    {id: 7, name: "item3"},
    {id: 8, name: "item3"},
    {id: 9, name: "item4"}
  ];
  let itemsRight = [];
  let myTestVAR;
  console.log(myTestVAR)
</script>


<UiCard icon="extension" title="Puzzle">
  <div class="lists-container" bind:clientHeight={myTestVAR}>
    <div class="list">
      <HorizontalList bind:items={itemsLeft} height={((myTestVAR)-100).toString()}/>
    </div>
    <div class="list">
      <HorizontalList bind:items={itemsRight} height={((myTestVAR)-100).toString()}/>
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
    align-items: center;
  }
  .list{
    flex: 1;
  }

</style>