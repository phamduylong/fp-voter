const mongoose = require("mongoose");
const bcrypt = require("bcrypt")
const Schema = mongoose.Schema;

//defining user schema
const userSchema = new Schema({
  username: { type: String, required: true },
  password: { type: String, required: true },
  id: { type: Number, required: true },
  fingerPrint: { type: String, required: false},
  candidateVotedFor: [{type: Schema.ObjectId, ref: 'candidate', required: false}],
  isAdmin: { type: Boolean, required: true},
});

userSchema.pre("save", async function(next) {
    if (!this.isModified("password")) return next();
    try {
      const salt = await bcrypt.genSalt(10);
      this.password = await bcrypt.hash(this.password, salt);
      return next();
    } catch (error) {
      return next(error);
    }
  });

//Export model
module.exports = mongoose.model("User", userSchema);
