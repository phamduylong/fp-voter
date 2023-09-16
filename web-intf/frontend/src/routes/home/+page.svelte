<script>
    import { onMount } from "svelte";
    import { AppBar , Avatar , AppRail, AppRailTile, AppRailAnchor } from '@skeletonlabs/skeleton';
    let test = [];

    onMount(async function() {
        const response = await fetch('http://localhost:8080/data');
        test = await response.json();
        console.log(test)
    });
</script>

<label class="label">
	<span>Input</span>
	<input class="input" type="text" placeholder="Input" />
    <span>Input</span>
	<input class="input" type="text" placeholder="Input" />
</label>

<ul>
    {#each test as t}
    <li>Username : {t.Username}    Recent Votes:{t.Vote}</li>
    {/each}
</ul>
