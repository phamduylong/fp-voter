<script>
    import jwt_decode from "jwt-decode";
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
            goto("/login");
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
                    res = await res.json();
                    console.info(res.message);
                    goto("/login");
                } else if (res.status === 401 || res.status === 500) {
                    goto("/login");
                }
            })
            .catch((err) => {
                // also a modal to tell user the error
                console.error(err);
            });
    }

    onMount(async () => {
        handleExpiredToken();
        if (!token) {
            goto("/login");
        } else {
            const currentUser = jwt_decode(token);
            console.log(currentUser);
        }
    });

    async function getCandidates() {
        await fetch("http://localhost:8080/candidates", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })
            .then(async (res) => {
                if (res.status == 401) {
                    res = await res.json();
                    console.error(res);
                    goto("/login");
                }
            })
            .catch((error) => {
                console.log("error", error);
            });
    }

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
                <li><a href="/home">Home</a></li>
                <li><a href="/vote">Vote</a></li>
                <li><a href="/home" on:click={getCandidates}>Get Candidates</a></li>
                <li><a href="/" on:click={handleLogout}>Logout</a></li>
            </ul>
        </nav>
    </svelte:fragment>

</AppShell>

<style>

</style>
