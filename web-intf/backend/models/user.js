const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const userSchema = new Schema({
  username: { type: String, required: true },
  password: { type: String, required: true },
  id: { type: Number, required: true },
  fingerprint: { type: Buffer, required: false},
  candidateVotedFor: {type: Schema.ObjectId, ref: 'Candidate', required: false},
  isAdmin: { type: Boolean, required: true},
});

//Export model
module.exports = mongoose.model("User", userSchema);