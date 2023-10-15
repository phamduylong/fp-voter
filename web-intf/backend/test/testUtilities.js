const bcrypt = require("bcrypt");
const User = require("../models/User");



const createTestUser = async () =>{
    const username = "backendUnitTest";
    let password = "unitTest#0001";
    const salt = await bcrypt.genSalt();
    password = await bcrypt.hash(password, salt);
    const newUser = new User({ username: username, password: password, isAdmin: false });
    await newUser.save();
}


const deleteTestUser = async () =>{
   await User.findOneAndRemove({username: "backendUnitTest"});

}

module.exports = {createTestUser,deleteTestUser}