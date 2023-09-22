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
const Candidate = require('./models/candidate')
const User = require('./models/user')
const routes = require("./routes/routes");
const compression = require("compression");

/* MIDDLEWARES */

app.use(compression()); 
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(cookieParser());
app.use(cors())
dotenv.config()


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
app.use("/", routes);
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


app.listen(PORT) ;
