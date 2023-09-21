const mongoose = require('mongoose');
const dotenv = require('dotenv');
dotenv.config();
const User = require('./models/User');
const mongoUri = process.env.MONGODB_URI;
async function connectToDb() {
    await mongoose.connect(mongoUri).then(() => {
    console.log("connected to mongo");})
    .catch((error) => {
        console.log(error)
    });
}

async function addNewUser(username, password, isAdmin){
    const user = new User({
        username: username,
        password: password,
        id: Date.now(),
        isAdmin: isAdmin
    })
    await user.save().then((savedDoc) => {return savedDoc === user});
}

async function countUsersWithCriteria(criteria){
    return await User.countDocuments(criteria).then((count) => {return count}).catch((error) => {console.error(error);});
}

module.exports = { connectToDb, addNewUser, countUsersWithCriteria };