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
            clearInterval(intervalId);
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

<AppShell>
    <svelte:fragment slot="header">
        <AppBar
            >FP Voter <button on:click={handleLogout} id="logoutBtn"
                >Logout</button
            ></AppBar
        >
    </svelte:fragment>
    <svelte:fragment slot="sidebarLeft">
        <div id="sidebar-left" class="hidden lg:block">
            This should be a sidebar
        </div>
    </svelte:fragment>
    <button on:click={getCandidates} id="getCandidateBtn">Get Candidates</button
    >
</AppShell>

<style>
    #logoutBtn {
        left: 1450%;
        position: relative;
    }
</style>
