// flavorModule.js
const { gql } = require('apollo-server-express');
const Flavor = require('./models/flavor');

// 1. Definición del Esquema (typeDefs) basados en la web de Frío Natural
const flavorTypeDefs = gql`
    type Flavor {
        id: ID!
        name: String!
        category: String!
        price: Float!
        tag: String
        stockKg: Float!
    }

    input FlavorInput {
        name: String!
        category: String!
        price: Float!
        tag: String
        stockKg: Float!
    }

    type Alert {
        message: String!
    }

    extend type Query {
        getFlavors: [Flavor]
        getFlavorById(id: ID!): Flavor
    }

    extend type Mutation {
        addFlavor(input: FlavorInput!): Flavor
        updateFlavor(id: ID!, input: FlavorInput!): Flavor
        deleteFlavor(id: ID!): Alert
    }
`;

// 2. Definición de los Resolvers conectados a MongoDB
const flavorResolvers = {
    Query: {
        getFlavors: async () => {
            try {
                return await Flavor.find();
            } catch (error) {
                throw new Error('Error al obtener los sabores de helado: ' + error.message);
            }
        },
        getFlavorById: async (_, { id }) => {
            try {
                const flavor = await Flavor.findById(id);
                if (!flavor) return null;
                return flavor;
            } catch (error) {
                throw new Error('Sabor no encontrado: ' + error.message);
            }
        }
    },
    Mutation: {
        addFlavor: async (_, { input }) => {
            try {
                const newFlavor = new Flavor(input);
                await newFlavor.save();
                return newFlavor;
            } catch (error) {
                throw new Error('Error al registrar el sabor: ' + error.message);
            }
        },
        updateFlavor: async (_, { id, input }) => {
            try {
                const updatedFlavor = await Flavor.findByIdAndUpdate(id, input, { new: true });
                return updatedFlavor;
            } catch (error) {
                throw new Error('Error al actualizar el sabor: ' + error.message);
            }
        },
        deleteFlavor: async (_, { id }) => {
            try {
                await Flavor.findByIdAndDelete(id);
                return { message: 'Sabor eliminado exitosamente de Frío Natural' };
            } catch (error) {
                throw new Error('Error al eliminar el sabor: ' + error.message);
            }
        }
    }
};

module.exports = { flavorTypeDefs, flavorResolvers };