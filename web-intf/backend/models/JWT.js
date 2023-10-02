const mongoose = require("mongoose");
const Schema = mongoose.Schema;
const JWTSchema = Schema({
    token: {type: String, required: true},
    expiryTime: { type: Number, required: true}
  });
  

module.exports = mongoose.model("JWT", JWTSchema);