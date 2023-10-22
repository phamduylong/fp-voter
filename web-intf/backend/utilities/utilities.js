const JWT = require('../models/JWT');
const jwt = require('jsonwebtoken');
const dotenv = require('dotenv');

dotenv.config();
const JWT_KEY = process.env.JWT_SECRET;

const checkJwtExpiration = async (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (token !== "null" && token !== undefined) {
        try {
            const decodedToken = jwt.verify(token, JWT_KEY);
            const tokenIsInactive = await checkInactiveToken(token);
            const currentTokenExpired = decodedToken.exp * 1000 < Date.now();
            if (tokenIsInactive || currentTokenExpired) {
                return res.status(401).json({ error: 'Session has expired. Please log in again.' });
            }
            req.user = decodedToken;
            next();
        } catch (err) {
            // in theory, this should not happen for ordinary users
            return res.status(401).json({ error: 'JWT malformed' });
        }
    } else {
        //token was not provided, user not logged in.
        return res.status(401).json({ error: 'You are not logged in.' });
    }
};
async function deleteExpiredTokens() {
    const tokens = await JWT.find({});
    tokens.forEach(async (token) => {
        if (token.expiryTime  < Date.now()) {
            await JWT.deleteOne({ _id: tokens._id });
        }
    });
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
    const passwordRegex = new RegExp(/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!*_])([A-Za-z\d@#$%^&+=!*_]){8,20}$/);
    const isPwdMatch = passwordRegex.test(password);
    return (isUsernameMatch && isPwdMatch)
}

module.exports = {checkJwtExpiration, checkUserValidations}
