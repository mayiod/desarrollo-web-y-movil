// models/flavor.js
const mongoose = require('mongoose');

const flavorSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
        unique: true
    },
    category: {
        type: String, // Ej: "Cremoso", "Frutal / Al Agua", "Chocolate"
        required: true
    },
    price: {
        type: Number,
        required: true
    },
    tag: {
        type: String, // Ej: "Más Vendido", "Nuevo", o vacío
        default: ""
    },
    stockKg: {
        type: Number,
        required: true
    }
});

module.exports = mongoose.model('Flavor', flavorSchema);

// completar al unir con sitio web de Frío Natural, agregando los campos necesarios para la gestión de sabores de helado.