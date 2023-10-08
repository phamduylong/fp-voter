const JWT = require('../models/JWT');


async function deleteExpiredTokens() {
    const tokens = await JWT.find({});
    for (let i = 0; i < tokens.length; i++) {
        if (tokens[i].expiryTime  < Date.now()) {
            await tokens[i].deleteOne({ _id: tokens[i]._id });
        }
    }
}
async function checkInactiveToken(token) {
    await deleteExpiredTokens();
    const inactiveToken = await JWT.find({ token: token });
    //Check if there's no inactive token
    if (inactiveToken.length === 0) {
        return false;
    }
    //Check if inactive token already expired
    return inactiveToken[0].expiryTime < Date.now()

}

function checkUserValidations(username, password){
    const usernameRegex = new RegExp(/^(?![\d_])(?!.*[^\w-]).{4,20}$/);
    const isUsernameMatch = usernameRegex.test(username);
    const passwordRegex = new RegExp(/^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d\s]).{8,20}$/);
    const isPwdMatch = passwordRegex.test(password);
    return (isUsernameMatch && isPwdMatch)

}

module.exports = {checkInactiveToken, checkUserValidations}
