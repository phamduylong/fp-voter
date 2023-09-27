<script>
    import jwt_decode from "jwt-decode";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { AppShell } from "@skeletonlabs/skeleton";
    import { AppBar } from "@skeletonlabs/skeleton";

    let token =
        typeof window !== "undefined" ? localStorage.getItem("jwt") : null;
    let intervalId;

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
            clearInterval(intervalId)
            goto("/login");
        }
    }

    function handleLogout() {
        localStorage.removeItem("jwt");
        token = null;
        goto("/login");
    }

    onMount(async () => {
        intervalId = setInterval(handleExpiredToken, 1000);
        if (!token) {
            goto("/login");
        } else {
            const currentUser = jwt_decode(token);
            console.log(currentUser);
        }

        return () => {
            clearInterval(intervalId);
        };
    });
</script>

<AppShell>
    <svelte:fragment slot="header">
        <AppBar>FP Voter <button on:click={handleLogout} id="logoutBtn">Logout</button></AppBar
        >
    </svelte:fragment>
    <svelte:fragment slot="sidebarLeft">
        <div id="sidebar-left" class="hidden lg:block">This should be a sidebar</div>
    </svelte:fragment>

    <!-- (sidebarRight) -->
    <!-- (pageHeader) -->
    <!-- Router Slot -->
    <slot />

    <!-- ---- / ---- -->
    <!-- (pageFooter) -->
    <!-- (footer) -->
</AppShell>

<style>
    #logoutBtn{
        left: 1450%;
        position: relative;
    }
</style>