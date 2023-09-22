const mongoose = require("mongoose");


const Schema = mongoose.Schema;

//defining canidate schema
const canidateSchema = new Schema({
  name: { type: String, required: true },
  age: { type: Number, required: true },
  id: { type: Number, required: true },
  message: { type: String, required: true},
});

//Export model
module.exports = mongoose.model("Canidate", canidateSchema);