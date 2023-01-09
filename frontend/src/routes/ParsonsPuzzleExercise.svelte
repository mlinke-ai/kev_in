<script>
    import {flip} from "svelte/animate";
    import {dndzone} from "svelte-dnd-action";
    import HorizontalList from "../lib/components/horizontalList.svelte";
    import Button from "@smui/button/src/Button.svelte";
    let itemsLeft = [
        {id: 1, name: "print(22 + 66 + sum([1,2,3]))"},
        {id: 2, name: "print(22)\n34"},
        {id: 3, name: "item3"},
        {id: 4, name: "item4"}
    ];
    let itemsRight = [];

    function submit(){
        console.log(itemsRight)
    }
    let peter
</script>


<div style="margin-top: 200px;">
    <div class="lists-container">
        <div class="list">
            <h2 align="center">Drag your elements</h2>
            <HorizontalList bind:items={itemsLeft} height="300"/>
        </div>
        <div class="list">
            <h2 align="center">Drop your Elements here</h2>
            <HorizontalList bind:items={itemsRight} height="300"/>
        </div>
    </div>
</div>


<Button color="primary" variant="raised">Reset</Button>
<Button color="primary" variant="raised" on:click={submit}>Submit</Button>
<style>
    
    .lists-container{
        margin-top: 100px;
        display: flex;
        flex-direction: row;
        justify-content: center;
    }
    .list{
        flex: 1;
    }
</style>

