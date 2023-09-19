<script>
    import { onMount } from "svelte";
    let strength = 0;
    let validations = [];
    let submit;
    let username;
    let password = "";
    $: props = {
        value: 0,
        max: 3,
    };
    let err_code = 0 
    let invalid



onMount(async function () {
  const response = await fetch("http://localhost:8080/login/user");
  err_code = await response.json();
  console.log(err_code);
  if(err_code == 1){
    invalid.innerText = "Error! Username Or Password Incorrect"
    invalid.style.color = "red"
  }
});


</script>

<main>
    <form
        id="main"
        method="post"
        action="http://localhost:8080/login/user"
    >
        <h1 id="login">Login</h1>
        <span id="invalid" bind:this={invalid}></span>
        <div class="field">
            <input
                type="username"
                name="username"
                class="input"
                placeholder=""
                bind:value={username}
                required
            />
            <label for="username" class="label">Username</label>
        </div>

        <div class="field">
            <input
                type="password"
                name="password"
                class="input"
                placeholder=""
                bind:value={password}

            />
            <label for="password" class="label">Password</label>
        </div>
        <a href="http://localhost:8081/register">
            <span id="createAccount">Click Here To Create An Account!</span>
        </a> 
        <button
            type="submit"
            id="submit"
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
    #main {
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
    .field {
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
    .field::after {
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

    .field:focus-within {
        border-color: transparent;
    }

    .field:focus-within::after {
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

    .field:focus-within .label,
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

    #createAccount{
        position: relative;
        left: 7vh; 
        margin-bottom: 10px;
        font-size: 20px;
        text-decoration: underline;
        color:blue;
    }

</style>