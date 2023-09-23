const express = require("express");
const router = express.Router();
//const Candidate = require('../models/candidate')
const User = require('../models/user')
//const mongoose = require('mongoose')
const bcrypt = require("bcrypt")

router.post('/register', async (req, res) => {
    let username = req.body.username
    let password = req.body.password
    console.log(username);

    try {
        const user = await User.find({ username: username })
        if (user.length == 0) {
            const newUser = new User({ username: username, password: password, id: 0, fingerPrint: "", canidateVoteFor: [], isAdmin: false });
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
        return res.status(500).send({ error: "Error" });
    }
})

router.post('/login', async (req, res) => {
    let username = req.body.username;
    let password = req.body.password;
    console.log(username);

    try {
        const user = await User.find({ username: username })
        if (user.length == 1) {
            const match = await bcrypt.compare(password,user[0].password);
            if(match){
                console.log(match)
                res.status(200).send()
            }else{
                return res.status(400).send({error: "Error: Incorrect Password!"})
            }
        }
        else if (user.length > 1) {
            return res.status(500).send({ error: "Error: Error logining user!" })
        } else if (user.length == 0) {
            return res.status(400).send({ error: "Error: User Not Found!" })
        }
    } catch (error) {
        console.log(error)
        return res.status(500).send({ error: error });
    }
});

module.exports = router;