<script>
    import { goto } from "$app/navigation";
    import { ProgressBar } from "@skeletonlabs/skeleton";
    let strength = 0;
    let validations = [];
    let submit;
    let username;
    let password = "";
    let invalid = ""
    $: passwordStrengthBar = {
        value: 0,
        max: 3,
        meter: "h-4 animate-pulse bg-red-600 h-2.5 rounded-full dark:bg-red-500"
    };

    function changePasswordStrengthBarColor(strength){
        switch (strength){
            case 0:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-red-600 h-2.5 rounded-full dark:bg-red-500";
                break;
            case 1:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-orange-600 h-2.5 rounded-full dark:bg-orange-500";
                break;
            case 2:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-yellow-600 h-2.5 rounded-full dark:bg-yellow-500";
                break;
            case 3:
                passwordStrengthBar.meter = "h-4 animate-pulse bg-green-600 h-2.5 rounded-full dark:bg-green-500";
                break;

        }
    }



    function validatePassword() {
        validations = [
            password.search(/[A-Za-z0-9]{5}/) > -1,
            password.search(/[A-Z]/) > -1,
            password.search(/[0-9]/) > -1,
        ];

        strength = validations.reduce((acc, cur) => acc + cur);
        passwordStrengthBar.value = strength;

        changePasswordStrengthBarColor(strength);

        if (strength === 3 && username !== "" && username !== undefined) {
            submit.disabled = false;
            submit.style = "border: 3px solid #73AD21;";
        } else {
            submit.disabled = true;
            submit.style = "border: 3px solid orangered;";
        }
    }

    async function postUserData(){
        const user = {username: username, password: password}
        const invalidWarning = document.getElementById("invalidWarning")
       await fetch("http://localhost:8080/register", {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(user), // body data type must match "Content-Type" header
        }).then(async (res) => {
            if(res.status === 200) {
                // handle with a message box along with a link to redirect to login page?
                await goto('/login')
            }else if(res.status === 400){
                res = await res.json()
                invalidWarning.innerText = res['error']
                invalidWarning.style.color = "red"
            }else if(res.status === 500){
                res = await res.json()
                invalidWarning.innerText = res['error']
                invalidWarning.style.color = "red"
            }
        }).catch(err => {
            // also a modal to tell user the error
            console.log(err)
        });

    }

</script>

<main>
    <form id="registerForm" on:submit|preventDefault={postUserData}>
        <h1 id="registerHeader">Register</h1>
        <span id="invalidWarning" bind:this={invalid}></span>

        <div class="inputField">
            <label class="label">
                <span>Username</span>
                <input class="input" title="Input username" type="text"  name="username" bind:value={username} on:input={validatePassword} required/>
            </label>
        </div>
        <div class="inputField">
            <label class="label">
                <span>Password</span>
                <input class="input" title="Input password" name="password" type="password" bind:value={password} on:input={validatePassword}  required/>
            </label>
        </div>

        <div id="loginContainer">
            <a href="http://localhost:8081/login">
                <span id="loginDirectionText">Already Having An Account? Click <a id="loginDirectionLink">Here</a> To Login!</span>
            </a>
        </div>

        <button disabled type="submit" id="submit" bind:this={submit} >Create Account!</button>
        <div class="strength">
            <ProgressBar
                    meter={passwordStrengthBar.meter}
                label="Progress Bar"
                value={passwordStrengthBar.value}
                max={passwordStrengthBar.max}
            />
        </div>

        <ul>
            <li>
                {validations[0] ? "✔️" : "❌"} Must be at least 5 characters
            </li>
            <li>
                {validations[1] ? "✔️" : "❌"} Must contain a capital letter
            </li>
            <li>{validations[2] ? "✔️" : "❌"} Must contain a number</li>
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

    #registerHeader {
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
    }

    .input {
        border: none;
        margin: 0;
        width: 100%;
        padding: 0.25rem 0;
        background: none;
        color: white;
        font-size: 1.2rem;
    }

    .inputField::after {
        content: "";
        position: relative;
        display: block;
        height: 4px;
        width: 100%;
        background: black;
        transform: scaleX(0);
        transform-origin: 0;
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



    .strength {
        display: flex;
        height: 20px;
        width: 100%;
    }

    #submit{
        border: 3px solid orangered;
    }

    #invalidWarning{
        position: relative;
        top: 3.5vh;
        text-align: center;
        left: 12vh;
        font-size: 20px;
    }

    #loginContainer{
        text-align: center;
    }

    #loginDirectionText{
        margin-bottom: 10px;
        font-size: 18px;
        color:white;
    }
    #loginDirectionLink{
        position: relative;
        margin-bottom: 10px;
        font-size: 20px;
        text-decoration: underline;
        color:white;
    }
</style>
