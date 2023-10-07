
<script>
    import { goto } from "$app/navigation";
    let submit;
    let username;
    let password = "";

    async function postUserData(){
        const user = {username: username, password: password}
       await fetch("http://localhost:8080/login", {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(user), // body data type must match "Content-Type" header
        }).then(async (res) =>  {
                const response = await res.json();
                const invalidWarning = document.getElementById("invalidWarning")
            switch (res.status) {
                case 200:
                    localStorage.setItem('jwt', response.token);
                    await goto('/home');
                    break;
                case 400:
                    invalidWarning.innerText = response['error'];
                    invalidWarning.style.color = "red";
                    break;
                case 401:
                    invalidWarning.innerText = response['error'];
                    invalidWarning.style.color = "red";
                    break;
                case 500:
                    invalidWarning.innerText = response['error'];
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
    <form id="loginForm" on:submit|preventDefault={postUserData}>
        <h1 id="loginHeader">Login</h1>
        <span id="invalidWarning"></span>
        <div class="inputField">
            <label class="label">
                <span>Username</span>
                <input class="input" title="Input username" type="text"  bind:value={username} required/>
            </label>
        </div>
        <div class="inputField">
            <label class="label">s
                <span>Password</span>
                <input class="input" title="Input password" type="password"  bind:value={password} required/>
            </label>
        </div>
        <div id="createAccountContainer">
            <a href="http://localhost:8081/register">
                <span id="createAccountText">Click <a id="createAccountLink">Here</a> To Create An Account!</span>
            </a>
        </div>
        <button
            type="submit"
            id="submitForm"
            bind:this={submit}
            style="border: 3px solid #73ad21;">Login</button
        >

    </form>
</main>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Kanit:wght@400;700&family=Montserrat&family=Roboto:wght@400;700&display=swap");
    * {
        font-family: "Kanit", sans-serif;
    }


    #loginForm {
        position: relative;
        --text-color: white;
        max-width: 500px;
        top: 10vh;
        left: 40%;
        border: 2px solid #73ad21;
        border-radius: 25px;
        background: none;
        padding: 20px;


    }

    #submitForm {
        border: 3px solid #73ad21;
        border-radius: 25px;
        background: none;
        padding: 15px;
        top: 80%;
        left: 28%;
        position: relative;
        font-weight: 700;
        width: 154px;
        display: inline-block;
        margin: 20px 10px 10px;
    }

    #loginHeader {
        left: 40%;
        position: absolute;
        text-align: center;
        font-size: 25px;
        font-weight: 700;
        
    }
    .inputField {
        width: 100%;
        position: relative;
        border-bottom: 2px dashed white;
        margin: 4rem auto 1rem;
        /* transition: 500ms; */
    }

    .input {
        border: none;
        margin: 0;
        width: 100%;
        padding: 0.25rem 0;
        background: none;
        color: white;
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
        transform-origin: 0;
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


    #invalidWarning{
        position: relative;
        top: 3.5vh;
        text-align: center;
        left: 12vh;
        font-size: 20px;
    }
    #createAccountContainer{
        text-align: center;
    }

    #createAccountText{
        margin-bottom: 10px;
        font-size: 18px;
        color:white;
    }
    #createAccountLink{
        position: relative;
        margin-bottom: 10px;
        font-size: 20px;
        text-decoration: underline;
        color:white;
    }

</style>