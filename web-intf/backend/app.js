const express = require('express');
const app = express();
const path = require('path');
const mqtt = require('mqtt');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const http = require('http');
const server = http.createServer(app);
const cors = require('cors')


/* MIDDLEWARES */

app.use(bodyParser.urlencoded({extended: true}));
app.use(cookieParser());
app.use(cors())
//app.set('view engine', 'ejs');
//app.set('views', path.join(__dirname, 'views'));





/* DEFINING CONSTRAINTS */
const PORT = process.env.PORT || 8080;
let username, password = ""
let error = 0


//Rendering to the login page


app.post('/register/user', async(req,res)=>{
    error = 0
    username = req.body.username
    password = req.body.password
    console.log(username,password)
    res.redirect('http://localhost:8081/login')
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
