const mongoose = require("mongoose");

const Schema = mongoose.Schema;

//defining user schema
const userSchema = new Schema({
  username: { type: String, required: true },
  password: { type: String, required: true },
  id: { type: Number, required: true },
  fingerPrint: { type: Buffer, required: false},
  candidateVotedFor: [{type: Schema.ObjectId, ref: 'candidate'}],
  isAdmin: { type: Boolean, required: true},
});

//Export model
module.exports = mongoose.model("user", userSchema);
