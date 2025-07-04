const mongoose = require('mongoose');

const AssignmentSchema = new mongoose.Schema({
  teacher: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  title: String,
  description: String,
  fileUrl: String,
  submissions: [{
    student: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    fileUrl: String,
    marks: Number
  }]
});

module.exports = mongoose.model('Assignment', AssignmentSchema);