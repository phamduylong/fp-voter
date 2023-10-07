
<script>
    import { goto } from "$app/navigation";
    let submit;
    let username;
    let password = "";

    function postUserData(){
        const user = {username: username, password: password}
       fetch("http://localhost:8080/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(user),
        }).then(async (res) =>  {
                const response = await res.json();
                const invalidWarning = document.getElementById("invalidWarning")
            switch (res.status) {
                case 200:
                    localStorage.setItem('jwt', response.token);
                    await goto('/home');
                    break;
                case 400:
                    invalidWarning.innerText = response.error;
                    invalidWarning.style.color = "red";
                    break;
                case 401:
                    invalidWarning.innerText = response.error;
                    invalidWarning.style.color = "red";
                    break;
                case 500:
                    invalidWarning.innerText = response.error;
                    invalidWarning.style.color = "red";
                    break;
            }
        
        }).catch(err => {
            // also a modal to tell user the error
            console.error(err);
        });

    }




</script>

<main>
    <div class="card absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-1/3 p-4">
        <h3 class="h3 m-4 text-center">Login</h3>
            <label class="label m-4">
                <p>Username</p>
                <input class="input" title="Input username" type="text"  bind:value={username} required/>
            </label>
            <label class="label m-4 mb-10">
                <p>Password</p>
                <input class="input" title="Input password" type="password"  bind:value={password} required/>
            </label>
            <button
            type="button"
            class="btn variant-filled ml-4 mr-4 mt-4 mb-4 absolute left-1/2 -translate-x-1/2 -translate-y-1/2"
            id="submitForm"
            on:click={postUserData}>Login</button>
            <br><br>
            <a href="http://localhost:8081/register" class="anchor m-4 absolute left-1/2 -translate-x-1/2 -translate-y-1/2">
                Not a user yet? Click here.
            </a>
            <br><br>
    </div>
</main>

<style>


</style>