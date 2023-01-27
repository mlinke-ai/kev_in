<script>
	import { flip } from 'svelte/animate';
	import { dndzone } from 'svelte-dnd-action';

    import Highlight from "svelte-highlight";
    import python from "svelte-highlight/languages/python";
    import github from "svelte-highlight/styles/atom-one-dark";
    
    export let items;
    const flipDurationMs = 300;
	function handleDndConsider(e) {
		items = e.detail.items;
	}
	function handleDndFinalize(e) {
        items = e.detail.items;
	}

  export let height = "";

</script>


<!-- Remove background color of highlighting -->
<svelte:head>
  {@html github}  
  {@html `<style> .hljs{background:none}</style>`}
</svelte:head>

<div 
    class="hListStyling"
    style={"height: " + height + "px;"}
    use:dndzone={{items: items, flipDurationMs: flipDurationMs, dropTargetStyle: {outline: "#D79922 solid 3px "}}} 
    on:consider={handleDndConsider} 
    on:finalize={handleDndFinalize}
    >
    {#each items as item(item.id)}
		<div animate:flip="{{duration: flipDurationMs}}" class="itembox">
			      <div style="border-right: 1px solid #ffffff;">
                {item.id}&nbsp;
            </div>
            <div>
                <Highlight language={python} code={item.name}/>
            </div>
    </div>
	  {/each}
</div>


<style lang="scss">
    @use "../../../variables" as theme;
    
    .hListStyling {
        padding: 0.3em;
        overflow: auto;
        min-height: 50px;
    }
    @media (prefers-color-scheme: dark) {
        .hListStyling{border: 1px solid theme.$primaryDark;}
    }
    @media (prefers-color-scheme: light) {
        .hListStyling{border: 1px solid theme.$primaryLight;}
    }


  .itembox {
    padding: 0.2em;
    display: flex;
    flex-direction: row;
    border: 1px solid white;
    border-radius: 5px;
    margin-top: 5px;
  }

</style>
