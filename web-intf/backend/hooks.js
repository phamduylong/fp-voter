const bcrypt = require("bcrypt")

function compareHashPassword(hashedPassword, password){

    bcrypt.compare(password,hashedPassword).then((result) => {
        console.log(result)
        return result;
    })
}

module.exports = { compareHashPassword };