const mongoose = require("mongoose");
const bcrypt = require("bcrypt")
const Schema = mongoose.Schema;
const Counter = require("./Counter");

const userSchema = new Schema({
  username: { type: String, required: true },
  password: { type: String, required: true },
  id: { type: Number, required: true, default: -1 },
  fingerPrint: { type: String, required: false, default: ""},
  candidateVotedId: {type: Number, required: false, default: null},
  isAdmin: { type: Boolean, required: true},
});

userSchema.pre("save", function(next) {
  Counter.findByIdAndUpdate({_id: 'userId'}, {$inc: { seq: 1} }).then((idCounter) => {
      this.id = idCounter.seq;
      next();
  }).catch((error) => {
    if(error){
      return next(error);
    }
  })
});


module.exports = mongoose.model("User", userSchema);
