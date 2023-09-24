const express = require("express");
const router = express.Router();
const User = require('../models/User');
const bcrypt = require("bcrypt");

router.post('/register', async (req, res) => {
    const username = req.body.username;
    let password = req.body.password;

    try {
        const user = await User.find({ username: username });
        if (user.length === 0) {
            const salt = await bcrypt.genSalt(10);
            password = await bcrypt.hash(password, salt);
            const newUser = new User({ username: username, password: password, isAdmin: false });
            let userSaved = await newUser.save();
            if (userSaved != {}) {
                res.status(200).send({ message: "User saved successfully!" });
            }
            else {
                return res.status(500).send({ error: "Unable To Create User!" });
            }
        } else {
            return res.status(400).send({ error: "Error: User already exists!" });
        }
    } catch (error) {
        console.log(error);
        return res.status(500).send({ error: "Unable To Create User!" });
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
                res.status(200).send({ message: "Login successful!" });
            }else{
                return res.status(400).send({error: "Error: Incorrect Password!"})
            }
        }
        else if (user.length > 1) {
            return res.status(500).send({ error: "Error: Multiple Username exists!" });
        } else if (user.length === 0) {
            return res.status(400).send({ error: "Error: User Not Found!" });
        }
    } catch (error) {
        return res.status(500).send({ error: "Error: Unable To Login!" });
    }
});

//Put route to change user password
module.exports = router;