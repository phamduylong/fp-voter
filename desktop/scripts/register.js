window.addEventListener("load", () => {
    const registerBtn = document.getElementById("register-submit-btn");
    const dialog = document.querySelector("#register-dialog");
    const errMsg = document.querySelector("#err-msg");
    const dialogAgreeBtn = document.querySelector("#dialog-agree-button");
    dialogAgreeBtn.addEventListener("click", async () => {
        errMsg.innerHTML = "";
        await dialog.close();
    });

/**
  * Validate user inputs. Errors will be handled with a dialog.
  * @param {string} username 
  * @param {string} password 
  * @throws {Error} if inputs are malformed
  */
    const validateCredentials = (username, password) => {
    if (username === null || username === undefined || username.length === 0) {
        throw new Error("Username is missing!");
    }

    if (password === null || password === undefined || password.length === 0) {
        throw new Error("Password is missing!");
    }

    // ^ and $ ensure that the regular expression matches the entire input string, not just a part of it
    // (?![\d_]) ensures the username doesn't start with a digit (\d) or an underscore (_). 
    // (?!.*[^\w-]) checks for the absence of any character that is not a word character (\w) or whitespace character
    // (\s). helps prevent SQL injection and JSON injection by disallowing characters that are commonly used for injection attacks.
    // .{4,20} is a quantifier that ensures the username is between 4 and 20 characters long.
    const uidRegex = /^(?![\d_])(?!.*[^\w-]).{4,20}$/;

    // (?=.*[A-Za-z]) checks for the presence of at least one letter
    // (?=.*\d) checks for the presence of at least one digit
    // (?=.*[@#$%^&+=!*_]) checks for the presence of at least one special character
    // [A-Za-z\d@#$%^&+=!*_] matches any letter, digit, or special character
    // {8,20} is a quantifier that ensures the password is between 8 and 20 characters long.
    const pwdRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@#$%^&+=!*_])([A-Za-z\d@#$%^&+=!*_]){8,20}$/;

    if (!uidRegex.test(username)) {
        throw new Error("Username format is invalid!");
    }

    if (!pwdRegex.test(password)) {
        throw new Error("Password format is invalid!");
    }
 }

 /**
  * Make a request to server to register a new user. Errors will be handled with a dialog.
  * @param {string} username 
  * @param {string} password 
  * @throws {Error} if inputs are invalid/server sends an error through
  * @summary Attempts to register a new user.
  */
 const attemptRegister = (username, password) => {
    fetch("http://localhost:8080/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "referrer-policy": "no-referrer",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({ username: username, password: password })
    }).then(async (res) => {
        const resBody = await res.json();
    
        switch(res.status) {
            case 200:
                window.location.href = "./login.html";
                break;
            case 400:
                if (resBody.error) throw new Error(resBody.error);
                else throw new Error("User already exists!");
            case 500:
                if (resBody.error) throw new Error(resBody.error);
                else throw new Error("Internal Server Error!");
        }
    }).catch(async (err) => {
        console.log(err);
        // prevent dialog spamming and empty dialogs
        if (errMsg.innerHTML !== err.message && err.message && err.message !== "") {
            errMsg.innerHTML = err.message;
            await dialog.showModal();
        }
        
    });
 }

    window.onkeydown = (e) => {
        if (e.key === "Enter") {
            registerBtn.click();
        }
    }

/**
  * Attempt to register a new user. First user inputs are validated, then the request is sent to the server.
  * @throws {Error} if inputs are invalid/server sends an error through.
  * @summary Registers a new user.
  */
    registerBtn.addEventListener("click", () => {
        const username = document.querySelector("#uid").value;
        const password = document.querySelector("#pwd").value;
        try {
            validateCredentials(username, password);
            attemptRegister(username, password);
        } catch (err) {
            if (errMsg.innerHTML !== err.message && err.message && err.message !== "") {
                errMsg.innerHTML = err.message;
                dialog.showModal();
            }
        }
    });


})