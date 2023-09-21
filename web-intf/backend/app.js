const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');
const dotenv = require('dotenv');
const { connectToDb, addNewUser, countUsersWithCriteria } = require('./hooks');

app.use(bodyParser.urlencoded({extended: true}));
app.use(cors());

/* MIDDLEWARES */
dotenv.config()
app.use(bodyParser.json());

app.all('*', function (req, res, next) {
    res.set({
        "Connection": "Keep-Alive",
        "Keep-Alive": "timeout=5, max=1000",
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
   });
    next();
});

const PORT = process.env.PORT || 8080;
connectToDb();

app.post('/register', async(req, res) => {
    const username = req.body.username;
    const password = req.body.password;
    const criteria = {username: username};
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
app.listen(PORT) ;
