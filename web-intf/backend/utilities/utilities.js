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

module.exports = {checkInactiveToken}
