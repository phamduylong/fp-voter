const mongoose = require("mongoose");
const Counter = require('./Counter')

const Schema = mongoose.Schema;

const candidateSchema = new Schema({
  name: { type: String, required: true },
  age: { type: Number, required: true },
  id: { type: Number, required: true},
  message: { type: String, required: true},
});

candidateSchema.pre("save", function(next) {
  Counter.findByIdAndUpdate({_id: 'candidateId'}, {$inc: { seq: 1} }).then((idCounter) => {
      this.id = idCounter.seq;
      next();
  }).catch((error) => {
    if(error){
      return next(error);
    }
  })
});


module.exports = mongoose.model("Candidate", candidateSchema);