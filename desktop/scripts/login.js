window.addEventListener("load", () => {
    const loginBtn = document.getElementById("login-submit-btn");
    const dialog = document.querySelector("#login-dialog");
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
    const validateLoginCredentials = (username, password) => {
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
  * Make a request to server to log a user in. Errors will be handled with a dialog.
  * @param {string} username 
  * @param {string} password 
  * @throws {Error} if inputs are invalid/server sends an error through.
  */
    const attemptLogin = (username, password) => {
        fetch("http://localhost:8080/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "referrer-policy": "no-referrer",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify({ username: username, password: password })
        }).then(async (res) => {
            const resBody = await res.json();
            switch (res.status) {
                case 200:
                    window.localStorage.setItem("token", resBody.token);
                    window.location.href = "./home.html";
                    break;
                case 401:
                    if (resBody.error) throw new Error(resBody.error);
                    else throw new Error("Username or password is incorrect!");
                case 500:
                    if (resBody.error) throw new Error(resBody.error);
                    else throw new Error("Internal Server Error!");
            }

        }).catch(async (err) => {
            if (errMsg.innerHTML !== err.message && err.message && err.message !== "") {
                errMsg.innerHTML = err.message;
                await dialog.showModal();
            }
        });
    }

    window.onkeydown = (e) => {
        if (e.key === "Enter") {
            loginBtn.click();
        }
    }

    loginBtn.addEventListener("click", async () => {
        const username = document.querySelector("#uid").value;
        const password = document.querySelector("#pwd").value;
        try {
            validateLoginCredentials(username, password);
            attemptLogin(username, password);
        } catch (err) {
            if (errMsg.innerHTML !== err.message && err.message && err.message !== "") {
                errMsg.innerHTML = err.message;
                await dialog.showModal();
            }
        }
    });
})