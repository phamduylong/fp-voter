<script>
    import { onMount } from "svelte";

    let submit;
    let username;
    let password = "";
    let errCode = 0 
    let invalid



onMount(async function () {
  const response = await fetch("http://localhost:8080/login/user");
  errCode = await response.json();
  console.log(errCode);
  if(errCode == 1){
    invalid.innerText = "Error! Username Or Password Incorrect"
    invalid.style.color = "red"
  }
});


</script>

<main>
    <form
        id="loginForm"
        method="post"
        action="http://localhost:8080/login/user"
    >
        <h1 id="login">Login</h1>
        <span id="invalid" bind:this={invalid}></span>
        <div class="inputField">
            <input
                type="text"
                name="username"
                class="input"
                bind:value={username}
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

            />
            <label for="password" class="label">Password</label>
        </div>
        <a href="http://localhost:8081/register">
            <span id="createAccountLink">Click Here To Create An Account!</span>
        </a> 
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
        --text-color: black;
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
        margin: 10px;
        left: 28%;
        position: relative;
        font-weight: 700;
        width: 154px;
        display: inline-block;
        margin-top: 20px;
    }

    #login {
        left: 40%;
        position: absolute;
        text-align: center;
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

    #invalid{
        position: relative;
        top: 4vh;
        text-align: center;
        left: 8vh;
    }

    #createAccountLink{
        position: relative;
        left: 7vh; 
        margin-bottom: 10px;
        font-size: 20px;
        text-decoration: underline;
        color:blue;
    }

</style>