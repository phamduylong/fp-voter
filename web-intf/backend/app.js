const express = require('express');
const app = express();
const path = require('path');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const http = require('http');
const server = http.createServer(app);
const cors = require('cors')
const mongoose = require('mongoose')
const { MongoClient, ServerApiVersion } = require('mongodb');
const dotenv = require('dotenv')
const Canidate = require('./models/canidate')
const User = require('./models/user')

/* MIDDLEWARES */

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(cookieParser());
app.use(cors())
dotenv.config()






/* DEFINING CONSTRAINTS */
const PORT = process.env.PORT || 8080;
const mongoUri = process.env.MONGODB_URI
console.log(mongoUri)
async function connectToDB() {
    await mongoose.connect(mongoUri)
    .catch((error) => {
        console.log(error)
    });
    
  }
connectToDB();


//Rendering to the login page

/*
app.post('/register', async(req, res) => {
    const username = req.body.username;
    const password = req.body.password;
    const criteria = {username: username};
    console.log(username)
    try {
        const userExist = await countUsersWithCriteria(criteria) > 0;
        if (!userExist) {               
            const userSaved = addNewUser(username, password, false);
            if (userSaved) return res.status(200).send({message: "User saved successfully"});
            else return res.status(500).send({error: "Error saving user"});
        } else {
            return res.status(400).send({error: "User already exists"});
        }
    } catch (error) {
        return res.status(500).send({error: error});
    }
});
*/

app.post('/register', async(req,res)=>{
    username = req.body.username
    password = req.body.password
    const criteria = {username: username};
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

app.post('/login/user', async(req,res)=>{
    let loginName = req.body.username
    let loginPassword = req.body.password
    if(loginName == username && loginPassword == password){
        res.redirect('http://localhost:8081/home')
        error = 0
    }else{
        error = 1
        res.redirect('http://localhost:8081/login')
    }
})

app.get('/login/user',async(req,res) =>{
    res.json(error)
})


server.listen(PORT) ;
