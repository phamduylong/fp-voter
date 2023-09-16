<script>
    import { onMount } from "svelte";

    let test = [];

    onMount(async function() {
        const response = await fetch('http://localhost:8080/data');
        test = await response.json();
        console.log(test)
    });
</script>
<h1>Combining SvelteKit and Golang server</h1>

<ul>
    {#each test as t}
    <li>{t.artist}</li>
    {/each}
</ul>
