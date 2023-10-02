const JWT = require('../models/JWT');


async function deleteExpiredTokens() {
    const tokens = await JWT.find({});
    for (let i = 0; i < tokens.length; i++) {
        if (tokens[i].expiryTime * 1000 < Date.now()) {
            await tokens[i].deleteOne({ _id: tokens[i]._id });
        }
    }
}
async function checkInactiveToken(token) {
    deleteExpiredTokens();
    const inactiveToken = await JWT.find({ token: token });
    //Check if theres no inactive token
    if (inactiveToken.length === 0) {
        return false;
    } else {
        //Check if inactive token already expired
        if (inactiveToken[0].expiryTime * 1000 < Date.now()) {
            return false;
        } else if (inactiveToken[0].expiryTime * 1000 > Date.now()) {
            return true;
        }
    }
}

module.exports = {checkInactiveToken}
