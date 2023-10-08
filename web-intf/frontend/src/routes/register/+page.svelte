<script>
    import { goto } from "$app/navigation";
    import { ProgressBar } from "@skeletonlabs/skeleton";
    let usernameStrength = 0;
    let passwordStrength = 0;
    let usernameValidations = [];
    let passwordValidations = [];
    let username = "";
    let password = "";
    let alertVisible = false;
    let alertMessage = "";
    $: passwordStrengthBar = {
        value: 0,
        max: 7,
        meter: "h-4 animate-pulse bg-red-600 h-2.5 rounded-full dark:bg-red-500"
    };

    // button is disabled if username or password is empty or password passwordStrength is less than 4 or usernameStrength is less than 3
    $: credentialsMissing = username === "" || password === "" || passwordStrength < 4 || usernameStrength < 3;

    const hideAlertTimeout = () => {
        setTimeout(() => {
            alertVisible = false;
        }, 3000);
    };

    const hideAlert = () => {
        alertVisible = false;
        clearTimeout(hideAlertTimeout);
    };

    function changePasswordStrengthBarColor(Strength){
        switch (Strength){
            case 0 || 1 :
                passwordStrengthBar.meter = "h-4 animate-pulse bg-red-600 h-2.5 rounded-full dark:bg-red-500";
                break;
            case 2 || 3:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-orange-600 h-2.5 rounded-full dark:bg-orange-500";
                break;
            case 4 || 5 || 6:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-yellow-600 h-2.5 rounded-full dark:bg-yellow-500";
                break;
            case 7:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-green-600 h-2.5 rounded-full dark:bg-green-500";
                break;

        }
    }

    function validateUsernameAndPassword() {

        usernameValidations = [
            username.search(/^(?![\d_])/) > -1,
            username.search(/^(?!.*[^\w-])/) > -1,
            username.search(/^.{4,20}$/) > -1,
        ];
        passwordValidations = [
            password.search(/^.{8,20}$/) > -1,
            password.search(/[A-Z]/) > -1,
            password.search(/[0-9]/) > -1,
            password.search(/[@#$%^&+=!*_]/) > -1,
        ];
        usernameStrength = usernameValidations.reduce((acc, cur) => acc + cur);
        passwordStrength = passwordValidations.reduce((acc, cur) => acc + cur);
        passwordStrengthBar.value = passwordStrength + usernameStrength;

        changePasswordStrengthBarColor(passwordStrengthBar.value);
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
            <input class="input" title="Input username" type="text"  name="username" bind:value={username} on:input={validateUsernameAndPassword}/>
        </label>
        <label class="label m-4 mb-10">
            <span>Password</span>
            <input class="input" title="Input password" name="password" type="password" bind:value={password} on:input={validateUsernameAndPassword}/>
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
                {usernameValidations[0] ? "✅" : "❌"} Username must not start with a digit or an underscore
            </li>
            <li>
                {usernameValidations[1] ? "✅" : "❌"} Username should not contain whitespace or special characters
            </li>
            <li>
                {usernameValidations[2] ? "✅" : "❌"} Username must be between 4 and 20 characters long
            </li>
            <li>
                {passwordValidations[0] ? "✅" : "❌"} Password must be between 8 and 20 characters long
            </li>
            <li>
                {passwordValidations[1] ? "✅" : "❌"} Password must contain a capital letter
            </li>
            <li>
                {passwordValidations[2] ? "✅" : "❌"} Password must contain a number
            </li>
            <li>
                {passwordValidations[3] ? "✅" : "❌"} Password must contain at a special character
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
