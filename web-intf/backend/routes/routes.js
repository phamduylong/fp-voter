const express = require("express");
const router = express.Router();
const Candidate = require('../models/candidate')
const User = require('../models/user')

//Rendering to the login page

router.post('/register', async(req,res)=>{
    username = req.body.username
    password = req.body.password
    console.log(username)
   try {
        const user = await User.find({username: username})
        if (!user) {               
            const userSaved = addNewUser(username, password, false);
            if (userSaved) return res.status(200).send({message: "User saved successfully!"});
            else return res.status(500).send({error: "Error: Error saving user!"});
        } else {
            return res.status(400).send({error: "Error: User already exists!"});
        }
    } catch (error) {
        return res.status(500).send({error: error});
    }
})

router.post('/login/user', async(req,res)=>{
    let loginName = req.body.username
    let loginPassword = req.body.password
    if(loginName == username && loginPassword == password){
        res.redirect('http://localhost:8081/home')
        error = 0
    }else{
        error = 1
        res.redirect('http://localhost:8081/login')
    }
});

module.exports = router;