window.addEventListener("load", () => {
    const loginBtn = document.getElementById("login-submit-btn");
    const validateLoginCredentials = (username, password) => {
    if (username === null || username === undefined || username.length < 4) {
        throw new Error("Username is missing or too short!");
    }

    if (password === null || password === undefined || password.length < 8) {
        throw new Error("Password is missing or too short!");
    }

    // ^ and $ ensure that the regular expression matches the entire input string, not just a part of it
    // (?![\d_]) ensures the username doesn't start with a digit (\d) or an underscore (_). 
    // (?!.*[^\w\s]) checks for the absence of any character that is not a word character (\w) or whitespace character
    // (\s). helps prevent SQL injection and JSON injection by disallowing characters that are commonly used for injection attacks.
    // .{4,20} is a quantifier that ensures the username is between 4 and 20 characters long.
    const uidRegex = /^(?![\d_])(?!.*[^\w\s]).{4,20}$/;

    // (?=.*[A-Za-z]) checks for the presence of at least one letter
    // (?=.*\d) checks for the presence of at least one digit
    // (?=.*[@#$%^&+=!*_]) checks for the presence of at least one special character
    // [A-Za-z\d@#$%^&+=!*_] matches any letter, digit, or special character
    // {8,20} is a quantifier that ensures the password is between 8 and 20 characters long.
    const pwdRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@#$%^&+=!*_])[A-Za-z\d@#$%^&+=!*_]{8,20}$/;

    if (!uidRegex.test(username)) {
        throw new Error("Username format is invalid!");
    }

    if (!pwdRegex.test(password)) {
        throw new Error("Password format is invalid!");
    }
 }

    loginBtn.addEventListener("click", () => {
        const username = document.querySelector("#uid").value;
        const password = document.querySelector("#pwd").value;
        const dialog = document.querySelector("#login-dialog");
        const errElem = document.querySelector("#err-msg");
        const dialogAgreeBtn = document.querySelector("#dialog-agree-button");
        dialogAgreeBtn.addEventListener("click", () => {
            dialog.close();
        });
        try {
            validateLoginCredentials(username, password);
        } catch (err) {
            errElem.innerHTML = err.message;
            dialog.showModal();
        }
    });
})