const JWT = require('../models/JWT');
const jwt = require('jsonwebtoken');
const dotenv = require('dotenv');


dotenv.config();
const JWT_KEY = process.env.JWT_SECRET;

const checkJwtExpiration = async (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (token) {
        try {
            const decodedToken = jwt.verify(token, JWT_KEY);
            const matchToken = await checkInactiveToken(token);

            if (matchToken === true) {
                return res.status(401).json({ message: 'Token is inactive' });
            }
            else if (decodedToken.exp * 1000 < Date.now()) {
                // Token has expired, send a 401 Unauthorized response
                return res.status(401).json({message: 'Token has expired'});
            }

            // Token is still valid, continue with the request
            req.user = decodedToken;
            next();
        } catch (err) {
            return res.status(401).json({ message: 'Invalid token' });
        }
    } else {
        return res.status(401).json({ message: 'Token not provided' });
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
