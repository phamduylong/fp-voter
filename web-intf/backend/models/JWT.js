const mongoose = require("mongoose");
const Schema = mongoose.Schema;
const JWTSchema = new Schema({
    token: {type: String, required: true},
    expiryTime: { type: Date, required: true}
  });
  

module.exports = mongoose.model("JWT", JWTSchema);