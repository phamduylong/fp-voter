<script>
    import { goto } from "$app/navigation";
    let alertVisible = false;
    let alertMessage = "";
    let usernameFormatInvalid = false;
    let passwordFormatInvalid = false;
    const usernameRegex = /^(?![\d_])(?!.*[^\w-]).{4,20}$/;
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@#$%^&+=!*_])([A-Za-z\d@#$%^&+=!*_]){8,20}$/;
    let username = "";
    let password = "";

    $: usernameFormatInvalid = !usernameRegex.test(username);
    $: passwordFormatInvalid = !passwordRegex.test(password);
    $: credentialsValid = username === "" || password === "" || usernameFormatInvalid || passwordFormatInvalid;

    const hideAlertTimeout = () => {
        setTimeout(() => {
            alertVisible = false;
        }, 3000);
    };

    const hideAlert = () => {
        alertVisible = false;
        clearTimeout(hideAlertTimeout);
    };

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
            switch (res.status) {
                case 200:
                    localStorage.setItem('jwt', response.token);
                    await goto('/home');
                    break;
                
                // everything but 200 will be an error here    
                default:
                    alertVisible = true;
                    alertMessage = response.error;
                    hideAlertTimeout();
                    break;
            }
        
        }).catch(err => {
            alertVisible = true;
            alertMessage = err;
            hideAlertTimeout();
            console.error(err);
        });

    }
</script>

<main>
    <div class="card absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-1/3 p-4">
        <h3 class="h3 m-4 text-center">Login</h3>
            <label class="label m-4">
                <span>Username</span>
                <input class="input" title="Input username" type="text"  bind:value={username} />
            </label>
            <label class="label m-4 mb-10">
                <span>Password</span>
                <input class="input" title="Input password" type="password"  bind:value={password} />
            </label>
            <button disabled={credentialsValid}
            type="button"
            class="btn variant-filled mr-4 mt-4 mb-4 absolute left-1/2 -translate-x-1/2 -translate-y-1/2"
            id="submitForm"
            on:click={postUserData}>Login</button>
            <br><br>
            <a href="http://localhost:8081/register" class="anchor m-4 absolute left-1/2 -translate-x-1/2 -translate-y-1/2 w-3/4 text-center">
                Not a user yet? Register now.
            </a>
            <br><br>
    </div>

    {#if alertVisible}
    <aside class="alert variant-filled-error w-3/4 absolute top-[90%] left-1/2 -translate-x-1/2 -translate-y-1/2 h-auto">
        <div class="alert-message">
            <h3 class="h3">Error</h3>
            <p>{alertMessage}</p>
        </div>
        <div class="alert-actions"><button class="btn variant-filled font-bold" on:click={hideAlert}>X</button></div>
    </aside>
    {/if}
</main>