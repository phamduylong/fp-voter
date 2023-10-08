<script>
    import { goto } from "$app/navigation";
    import { ProgressBar } from "@skeletonlabs/skeleton";
    const usernameRegex = /^(?![\d_])(?!.*[^\w-]).{4,20}$/;
    let username = "";
    let password = "";
    let alertVisible = false;
    let alertMessage = "";
    $: passwordLengthSuffices = password.search(/^([A-Za-z\d@#$%^&+=!*_]){8,20}$/) > -1;
    $: passwordContainsCapitalLetter = password.search(/[A-Z]/) > -1;
    $: passwordContainsDigit = password.search(/[0-9]/) > -1;
    $: passwordContainsSpecialCharacter = password.search(/[@#$%^&+=!*_]/) > -1;
    $: passwordStrengthBar = {
        value: [passwordLengthSuffices, passwordContainsCapitalLetter, passwordContainsDigit, passwordContainsSpecialCharacter].filter(r => r === true).length,
        max: 4,
        meter: "h-4 animate-pulse bg-red-600 h-2.5 rounded-full dark:bg-red-500"
    };
    $: usernameFormatInvalid = !usernameRegex.test(username);
    $: credentialsMissing = username === "" || password === "" || passwordStrengthBar.value < 4 || usernameFormatInvalid;

    const hideAlertTimeout = () => {
        setTimeout(() => {
            alertVisible = false;
        }, 3000);
    };

    const hideAlert = () => {
        alertVisible = false;
        clearTimeout(hideAlertTimeout);
    };

    function updatePasswordStrengthBarColor() {
        console.log(passwordStrengthBar.value);
        switch (passwordStrengthBar.value) {
            case 0:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-red-600 h-2.5 rounded-full dark:bg-red-500";
                break;
            case 1:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-orange-600 h-2.5 rounded-full dark:bg-orange-500";
                break;
            case 2:
            case 3:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-yellow-600 h-2.5 rounded-full dark:bg-yellow-500";
                break;
            case 4:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-green-600 h-2.5 rounded-full dark:bg-green-500";
                break;
            default:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-red-600 h-2.5 rounded-full dark:bg-red-500";
                break;
        }
    }

    function postUserData(){
        const user = {username: username, password: password}
        fetch("http://localhost:8080/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(user), 
        }).then(async (res) =>  {
            const response = await res.json();
            switch (res.status) {
                case 200:
                   await goto('/login');
                   break;
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

    <div class="card absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-1/3 p-4 ">
        <h3 class="h3 m-4 text-center">Register</h3>
        <label class="label m-4">
            <span>Username</span>
            <input class="input" title="Input username" type="text"  name="username" bind:value={username}/>
        </label>
        <label class="label m-4 mb-10">
            <span>Password</span>
            <input class="input" title="Input password" name="password" type="password" bind:value={password} on:input={updatePasswordStrengthBarColor}/>
        </label>
        <button
                disabled={credentialsMissing}
                type="button"
                class="btn variant-filled mr-4 mt-4 mb-10 absolute left-1/2 -translate-x-1/2 -translate-y-1/2 "
                id="submitForm"
                on:click={postUserData}>Register</button>
                <br><br>
            <ProgressBar
                    class="my-4"
                    meter={passwordStrengthBar.meter}
                    label="Progress Bar"
                    value={passwordStrengthBar.value}
                    max={passwordStrengthBar.max}
            />

        <ul class="list m-4">
            <li>
                {passwordLengthSuffices ? "✅" : "❌"} Password must be between 8 and 20 characters long
            </li>
            <li>
                {passwordContainsCapitalLetter ? "✅" : "❌"} Password must contain a capital letter
            </li>
            <li>
                {passwordContainsDigit ? "✅" : "❌"} Password must contain a number
            </li>
            <li>
                {passwordContainsSpecialCharacter ? "✅" : "❌"} Password must contain at a special character
            </li>
        </ul>
        <br>
        <a href="http://localhost:8081/login" class="anchor m-4 absolute mb-10 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3/4 text-center">
            Already having an account? Click here to login!
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
