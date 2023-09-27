<script>
    import jwt_decode from "jwt-decode";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";

    let token =
        typeof window !== "undefined" ? localStorage.getItem("jwt") : null;

    function handleLogout() {
        localStorage.removeItem("jwt");
        token = null;
        goto("/login");
    }

    onMount(async () => {
        if (!token) {
            goto("/login");
        } else {
            const currentUser = jwt_decode(token);
            console.log(currentUser);
        }
    });

</script>

<h1>LOGIN</h1>
<button on:click={handleLogout}>Logout</button>
