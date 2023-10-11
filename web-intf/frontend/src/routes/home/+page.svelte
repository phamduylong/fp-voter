<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import {
    AppShell,
    ListBox,
    ListBoxItem,
    popup,
  } from "@skeletonlabs/skeleton";

  $: token = typeof window !== "undefined" ? localStorage.getItem("jwt") : null;

  let currentUser = "user";

  let comboboxValue = "";

  const popupCombobox = {
    event: "click",
    target: "popupCombobox",
    placement: "bottom",
    closeQuery: "",
  };

  onMount(async () => {
    const userId = sessionStorage.getItem("userId");
    fetch(`http://localhost:8080/user/id=${userId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
    })
      .then(async (res) => {
        const response = await res.json();
        if (res.status === 200) {
          currentUser = response.username;
        }
      })
      .catch((err) => {
        console.error(err);
      });
  });

  async function handleLogout() {
    await fetch("http://localhost:8080/logout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
    })
      .then(async (res) => {
        if(res.ok) localStorage.removeItem("jwt");
        sessionStorage.removeItem("userId");
        await goto("/login");
      })
      .catch((err) => {
        console.error(err);
      });
  }
</script>

<AppShell>
  <div slot="header">
    <nav class="list-nav flex justify-center w-full py-4 card">
      <a href="/home">Home</a>
      <a href="/vote">Vote</a>
      <a href="/results">Results</a>
      <a href="/candidates">Candidates</a>
      <button
        class="btn variant-filled absolute right-10 !bg-inherit hover:!bg-gray-800 !text-inherit border-2"
        use:popup={popupCombobox}
      >
        Hello, {currentUser}
        <div class="card py-2" data-popup="popupCombobox">
          <ListBox>
            <ListBoxItem
              bind:group={comboboxValue}
              name="medium"
              value="profile"
              ><a href="/profile" class="anchor hover:!bg-transparent"
                >Profile</a
              ></ListBoxItem
            >
            <ListBoxItem
              bind:group={comboboxValue}
              name="medium"
              value="logout"
              on:click={handleLogout}
            >
              <a
                class="anchor hover:!bg-transparent"
                href="/"
                on:click|preventDefault={handleLogout}>Logout</a
              >
            </ListBoxItem>
          </ListBox>
        </div>
      </button>
    </nav>
  </div>
</AppShell>

<style>
</style>
