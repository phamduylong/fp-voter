/**
 * The preload script runs before. It has access to web APIs
 * as well as Electron's renderer process modules and some
 * polyfilled Node.js functions.
 *
 * https://www.electronjs.org/docs/latest/tutorial/sandbox
 */
window.addEventListener('DOMContentLoaded', () => {
  const loginBtn = document.getElementById("login-submit-btn");
  const username = document.getElementById("uid").value;
  const password = document.getElementById("pwd").value;
  const validateLoginCredentials = (username, password) => {

    let validLoginCredentials = true;
    let errMsg = "";

    if (username === null || username === undefined || username.length < 4 || password === null || password === undefined || password.length < 8) {
      validLoginCredentials = false;
      errMsg = "Username is missing or too short!";
    }

    if (password === null || password === undefined || password.length < 8) {
      validLoginCredentials = false;
      errMsg = "Password is missing or too short!";
    }

    // ^ and $ ensure that the regular expression matches the entire input string, not just a part of it
    // (?![\d_]) ensures the username doesn't start with a digit (\d) or an underscore (_). 
    // (?!.*[^\w\s]) checks for the absence of any character that is not a word character (\w) or whitespace character
    // (\s). helps prevent SQL injection and JSON injection by disallowing characters that are commonly used for injection attacks.
    // .{4,20} is a quantifier that ensures the username is between 4 and 20 characters long.
    const uidRegex = "^(?![\d_])(?!.*[^\w\s]).{4,20}$";

    // (?=.*[A-Za-z]) checks for the presence of at least one letter
    // (?=.*\d) checks for the presence of at least one digit
    // (?=.*[@#$%^&+=!*_]) checks for the presence of at least one special character
    // [A-Za-z\d@#$%^&+=!*_] matches any letter, digit, or special character
    // {8,20} is a quantifier that ensures the password is between 8 and 20 characters long.
    const pwdRegex = "/^(?=.*[A-Za-z])(?=.*\d)(?=.*[@#$%^&+=!*_])[A-Za-z\d@#$%^&+=!*_]{8,20}$/";

    if (!username.test(uidRegex)) {
      validLoginCredentials = false;
      errMsg = "Username format is invalid!";
    }

    if (!password.test(pwdRegex)) {
      validLoginCredentials = false;
      errMsg = "Password format is invalid!";
    }

    if(!validLoginCredentials) throw new Error(errMsg);
  }
  loginBtn.addEventListener("click", () => {
    try {
      validateLoginCredentials(username, password);
    } catch (err) {
      // handle the error here with a dialog box and don't proceed the login process
    }
  });
})
