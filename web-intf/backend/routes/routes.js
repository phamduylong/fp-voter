const express = require("express");
const router = express.Router();
const User = require('../models/User');
const bcrypt = require("bcrypt");

router.post('/register', async (req, res) => {
    const username = req.body.username;
    const password = req.body.password;

    try {
        const user = await User.find({ username: username });
        if (user.length === 0) {
            const newUser = new User({ username: username, password: password, isAdmin: false });
            let userSaved = await newUser.save();
            if (userSaved != {}) {
                res.status(200).send({ message: "User saved successfully!" });
            }
            else {
                return res.status(500).send({ error: "Error: Error saving user!" });
            }
        } else {
            return res.status(400).send({ error: "Error: User already exists!" });
        }
    } catch (error) {
        console.log(error);
        return res.status(500).send({ error: "Server Internal Error" });
    }
})

router.post('/login', async (req, res) => {
    const username = req.body.username;
    const password = req.body.password;

    try {
        const user = await User.find({ username: username })
        if (user.length === 1) {
            const match = await bcrypt.compare(password,user[0].password);
            if(match){
                res.status(200).send()
            }else{
                return res.status(400).send({error: "Error: Incorrect Password!"})
            }
        }
        else if (user.length > 1) {
            return res.status(500).send({ error: "Error: Error logging in!" });
        } else if (user.length === 0) {
            return res.status(400).send({ error: "Error: User Not Found!" });
        }
    } catch (error) {
        return res.status(500).send({ error: "Server Internal Error" });
    }
});

//Put route to change user password
module.exports = router;