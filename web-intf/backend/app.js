const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const mongoose = require('mongoose');

const routes = require("./routes/routes");
const userRoutes = require("./routes/userRoutes");
const compression = require("compression");


/* MIDDLEWARES */

app.use(compression()); 
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(cookieParser());
app.use(cors());


/* MIDDLEWARES */

app.use(bodyParser.json());
const mongoUri = process.env.MONGODB_URI;
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
app.use("/user", userRoutes);
const PORT = process.env.PORT || 8080;

async function connectToDB() {
  mongoose.connect(mongoUri)
  .then(() => {
    console.info("Connected To Database!");
  })
  .catch((error) => {
    console.error(error);
  });
  
}
connectToDB();
module.exports = app.listen(PORT);

