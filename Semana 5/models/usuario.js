const mongoose = require('mongoose');
const usuarioSchema = new mongoose.Schema({
    nombre: {type: String, required: true},
    pass: {type: String, require: true}
});

module.exports = mongoose.model('Usuario', usuarioSchema);