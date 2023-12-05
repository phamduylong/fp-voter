<script>
    import { goto } from "$app/navigation";
    import { ProgressBar } from "@skeletonlabs/skeleton";
    import {alertState} from "$lib/alertStore.js";
    const usernameRegex = /^(?![\d_])(?!.*[^\w-]).{4,20}$/;
    let username = "";
    let password = "";
    const meters = ["","h-4 animate-pulse bg-red-600 h-2.5 rounded-full dark:bg-red-500", "h-4 animate-pulse bg-orange-600 h-2.5 rounded-full dark:bg-orange-500",
        "h-4 animate-pulse bg-orange-600 h-2.5 rounded-full dark:bg-yellow-500", "h-4 animate-pulse bg-orange-600 h-2.5 rounded-full dark:bg-green-500"];

    $: passwordLengthSuffices = password.search(/^([A-Za-z\d@#$%^&+=!*_]){8,20}$/) > -1;
    $: passwordContainsCapitalLetter = password.search(/[A-Z]/) > -1;
    $: passwordContainsDigit = password.search(/[0-9]/) > -1;
    $: passwordContainsSpecialCharacter = password.search(/[@#$%^&+=!*_]/) > -1;
    $: value = [passwordLengthSuffices, passwordContainsCapitalLetter, passwordContainsDigit, passwordContainsSpecialCharacter].filter(r => r === true).length;
    $: max = 4;
    $: meter = meters[value];

    $: usernameFormatInvalid = !usernameRegex.test(username);
    $: credentialsInvalid = username === "" || password === "" || value < 4 || usernameFormatInvalid;



    function postUserData(){

        const user = {username: username, password: password};
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
                    if(response.error){
                        alertState.show(response.error,"error");
                    }else{
                        alertState.show("Failed to register!","error");
                    }

                   break;
            }

       }).catch(err => {
           alertState.show();
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
            <input class="input" title="Input password" name="password" type="password" bind:value={password} />
        </label>
        <button
                disabled={credentialsInvalid}
                type="button"
                class="btn variant-filled mr-4 mt-4 mb-10 absolute left-1/2 -translate-x-1/2 -translate-y-1/2"
                id="submitForm"
                on:click={postUserData}>Register</button>
                <br><br>
            <ProgressBar
                    class="my-4"
                    {meter}
                    label="Progress Bar"
                    {value}
                    {max}
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


</main>
