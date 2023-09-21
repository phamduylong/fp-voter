<script>
    import { ProgressBar } from "@skeletonlabs/skeleton";
    import { onMount } from "svelte";
    let strength = 0;
    let validations = [];
    let submit;
    let username;
    let password = "";
    $: passwordStrengthBar = {
        value: 0,
        max: 3,
    };

    function validatePassword() {
        validations = [
            password.search(/[A-Za-z0-9]{5}/) > -1,
            password.search(/[A-Z]/) > -1,
            password.search(/[0-9]/) > -1,
        ];

        strength = validations.reduce((acc, cur) => acc + cur);
        passwordStrengthBar.value = strength;

        if (strength == 3 && username != "" && username != undefined) {
            submit.disabled = false;
            submit.style = "border: 3px solid #73AD21;";
        } else {
            submit.disabled = true;
            submit.style = "border: 3px solid orangered;";
        }
    }
    /*
    onMount(async function () {
        const response = await fetch("http://localhost:8080/register/user");
        errCode = await response.json();
        console.log(errCode)
        
    });
    */
    
    async function postUserData(){
        const user = {username: username, password: password}
        const response = await fetch("http://localhost:8000/register", {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            referrer: "about:client", // or "" to send no Referer header,
            // or an url from the current origin
            referrerPolicy: "no-referrer", // no-referrer-when-downgrade, no-referrer, origin, same-origin...
            mode: "cors", // same-origin, no-cors
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(user), // body data type must match "Content-Type" header
        });
        console.log(response.json()) // parses JSON response into native JavaScript objects
    }

    
</script>

<main>
    <form id="registerForm" on:submit|preventDefault={postUserData}>
        <h1 id="register">Register</h1>
        <div class="inputField">
            <input
                type="text"
                name="username"
                class="input"
                bind:value={username}
                on:input={validatePassword}
                required
            />
            <label for="username" class="label">Username</label>
        </div>

        <div class="inputField">
            <input
                type="password"
                name="password"
                class="input"
                bind:value={password}
                on:input={validatePassword}
            />
            <label for="password" class="label">Password</label>
        </div>
        <button
            type="submit"
            id="submit"
            disabled={true}
            bind:this={submit}
            style="border: 3px solid orangered;">Create Account!</button
        >
        <div class="strength">
            <ProgressBar
                label="Progress Bar"
                value={passwordStrengthBar.value}
                max={passwordStrengthBar.max}
            />
        </div>

        <ul>
            <li>
                {validations[0] ? "✔️" : "❌"} must be at least 5 characters
            </li>
            <li>
                {validations[1] ? "✔️" : "❌"} must contain a capital letter
            </li>
            <li>{validations[2] ? "✔️" : "❌"} must contain a number</li>
        </ul>
    </form>
</main>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Kanit:wght@400;700&family=Montserrat&family=Roboto:wght@400;700&display=swap");
    * {
        font-family: "Kanit", sans-serif;
    }
    #registerForm {
        position: relative;
        --text-color: black;
        max-width: 500px;
        top: 10vh;
        left: 40%;
        border: 2px solid #73ad21;
        border-radius: 25px;
        background: none;
        padding: 20px;
    }

    #submit {
        border: 3px solid #73ad21;
        border-radius: 25px;
        background: none;
        padding: 15px;
        margin: 10px;
        left: 28%;
        position: relative;
        font-weight: 700;
    }

    #register {
        left: 38%;
        position: absolute;
        font-size: 25px;
        font-weight: 700;
    }
    .inputField {
        width: 100%;
        position: relative;
        border-bottom: 2px dashed black;
        margin: 4rem auto 1rem;
        /* transition: 500ms; */
    }

    .input {
        border: none;
        margin: 0;
        width: 100%;
        padding: 0.25rem 0;
        background: none;
        color: black;
        font-size: 1.2rem;
        /* transition: border 500ms; */
    }

    /* border animation */
    .inputField::after {
        content: "";
        position: relative;
        display: block;
        height: 4px;
        width: 100%;
        background: black;
        transform: scaleX(0);
        transform-origin: 0%;
        /* opacity: 0; */
        transition: transform 500ms ease;
        top: 2px;
    }

    .inputField:focus-within {
        border-color: transparent;
    }

    .inputField:focus-within::after {
        transform: scaleX(1);
        opacity: 1;
    }

    /* label animation */
    .label {
        z-index: -1;
        position: absolute;
        transform: translateY(-2rem);
        transform-origin: 0%;
        transition: transform 400ms;
    }

    .inputField:focus-within .label,
    .input:not(:placeholder-shown) + .label {
        transform: scale(0.8) translateY(-5rem);
        opacity: 1;
    }

    /* strength meter */

    .strength {
        display: flex;
        height: 20px;
        width: 100%;
    }
</style>
