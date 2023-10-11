const express = require("express");
const userRouter = express.Router();
const User = require('../models/User');
const { checkJwtExpiration } = require('../utilities/utilities');
userRouter.get('/id=:id', checkJwtExpiration, async (req, res) => {
    const userId = req.params.id;
    if(userId === undefined || userId === null || userId < 0) {
        return res.status(400).send({ error: "User id is invalid!" });
    }
    try {
        const user = await User.find({ id: Number(userId) });
        if (user.length === 1) {
            const result = {
                username: user[0].username,
                isAdmin: user[0].isAdmin,
                id: user[0].id,
                fingerprintId: user[0].fingerprintId,
                sensorId: user[0].sensorId,
                candidateVotedId: user[0].candidateVotedId
            };
            return res.status(200).send( result );
        }
        return res.status(400).send({ error: "User Not Found!" });
    } catch (error) {
        return res.status(500).send({ error: error });
    }
});

module.exports = userRouter;