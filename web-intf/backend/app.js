const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const http = require('http');
const server = http.createServer(app);
const cors = require('cors')

// Middlewares
app.use(bodyParser.urlencoded({extended: true}));
app.use(cookieParser());
app.use(cors());


// Defining constants
const PORT = process.env.PORT || 8080;

app.post('/register/user', async(req,res)=>{
})

app.post('/login/user', async(req,res)=>{
})

app.get('/login/user',async(req,res) =>{
    
})


server.listen(PORT) ;
