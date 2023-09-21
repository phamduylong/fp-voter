const express = require('express');
const app = express();
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

// Middlewares
app.use(bodyParser.urlencoded({extended: true}));
app.use(cookieParser());
app.use(cors());

/* MIDDLEWARES */
dotenv.config()
app.use(bodyParser.urlencoded({extended: true}));
app.use(cookieParser());

app.all('*', function (req, res, next) {
    res.set({
        "Connection": "Keep-Alive",
        "Keep-Alive": "timeout=5, max=1000",
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
   });
    next();
});

//app.set('view engine', 'ejs');
//app.set('views', path.join(__dirname, 'views'));


// Defining constants
const PORT = process.env.PORT || 8080;
const mongoUri = process.env.MONGODB_URI
let username, password = ""
let error = 0
console.log(mongoUri)
async function connectToDB() {
    await mongoose.connect(mongoUri)
    .catch((error) => {
        console.log(error)
    });
    
  }
connectToDB();


//Rendering to the login page


app.post('/register', async(req,res)=>{
    username = req.body.username
    password = req.body.password
    console.log(username,password)
    let msg = {"error": "yo"}
    const user = await User.find({username: username})
    if (user == []){
        saveUserToDB(username,password,true)
    }else{
        res.set({
            "Connection": "Keep-Alive",
            "Keep-Alive": "timeout=5, max=1000",
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
        });
        return res.send(msg)
    }
})

app.get('/error', (req, res) => {
    res.redirect('http://localhost:8081/login');
  });





async function saveUserToDB(username,password,role){
    const user = new User({
        username: username,
        password: password,
        id: 0,
        isAdmin: role
    })
    await user.save();
}

server.listen(PORT) ;
