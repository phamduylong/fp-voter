<script>
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { AppShell } from "@skeletonlabs/skeleton";
    import { AppBar } from "@skeletonlabs/skeleton";

    let token =
        typeof window !== "undefined" ? localStorage.getItem("jwt") : null;

    function isTokenExpired(token) {
        if (!token) return true;
        const decodedToken = JSON.parse(atob(token.split(".")[1])); // Decode the token
        const expirationTime = decodedToken.exp * 1000;
        const currentTime = Date.now();
        return currentTime > expirationTime;
    }
    function handleExpiredToken() {
        if (isTokenExpired(token)) {
            localStorage.removeItem("jwt");
            token = null;
            window.location.href = "http://localhost:8081/login"
        }
    }

    async function handleLogout() {
        await fetch("http://localhost:8080/logout", {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        })
            .then(async (res) => {
                if (res.status === 200) {
                    localStorage.removeItem("jwt");
                    token = null;
                }
                await goto("/login");
            })
            .catch((err) => {
                // also a modal to tell user the error
                console.error(err);
            });
    }

    onMount(async () => {
        handleExpiredToken();
        if (!token) {
            await goto("/login");
        } else {
            const decodedToken = JSON.parse(atob(token.split(".")[1]));
            console.log(decodedToken.user);
        }
    });


</script>

<AppShell slotSidebarLeft="bg-surface-500/5 w-0 lg:w-64">
    <svelte:fragment slot="header">
        <AppBar
            ><strong class="text-xl uppercase">FP Voter</strong>

                </AppBar
        >
    </svelte:fragment>

    <svelte:fragment slot="sidebarLeft">
        <nav class="list-nav">
            <ul>
                <li><a href="/home" on:click={handleExpiredToken}>Home</a></li>
                <li><a href="/vote" on:click={handleExpiredToken}>Vote</a></li>
                <li><a href="/" on:click={handleLogout}>Logout</a></li>
            </ul>
        </nav>
    </svelte:fragment>

</AppShell>

<style>

</style>
