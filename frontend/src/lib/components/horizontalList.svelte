<script>
	import { flip } from 'svelte/animate';
	import { dndzone } from 'svelte-dnd-action';

    import Highlight from "svelte-highlight";
    import python from "svelte-highlight/languages/python";
    import github from "svelte-highlight/styles/atom-one-dark";
    import { linear } from 'svelte/easing';
    
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

<style lang="scss">
    @use "../../variables" as theme;
    
    section {
        padding: 0.3em;
        overflow: auto;
    }
    @media (prefers-color-scheme: dark) {
        section{border: 1px solid theme.$primaryDark;}
    }
    @media (prefers-color-scheme: light) {
        section{border: 1px solid theme.$primaryLight;}
    }


	.itembox {
		padding: 0.2em;
		margin: 0.15em 0;
        display: flex;
        flex-direction: row;
        border: 1px solid white;
	}

</style>

<!-- Remove background color of highlighting -->
<svelte:head>
  {@html github}  
  {@html `<style> .hljs{background:none}</style>`}
</svelte:head>

<section style={"height: "+height + "px"} use:dndzone={{items, flipDurationMs}} on:consider={handleDndConsider} on:finalize={handleDndFinalize}>
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
</section>
{items}
