const { gql } = require('apollo-server-express');
const Usuario = require('./models/usuario');

const usuarioTypeDefs = gql`
    type Usuario {
        id: ID!
        nombre: String!
        pass: String!
    }

    input UsuarioInput {
        nombre: String!
        pass: String!
    }

    type Alert {
        message: String!
    }
        
    extend type Query {
        getUsuarios: [Usuario]
        getUsuarioById(id: ID!): Usuario
    }

    extend type Mutation {
        addUsuario(input: UsuarioInput!): Usuario
        updUsuario(id: ID!, input: UsuarioInput!): Usuario
        delUsuario(id: ID!): Alert
    }

`;

const usuarioResolvers = {
    Query: {
        getUsuarios: async () => {
            return await Usuario.find();
        },
        getUsuarioById: async (_, { id }) => {
            const usuarioBus = await Usuario.findById(id);
            if (usuarioBus === null) return null;
            return usuarioBus;
        }
    },
    Mutation: {
        addUsuario: async (_, { input }) => {
            const nuevoUsuario = new Usuario(input);
            await nuevoUsuario.save();
            return nuevoUsuario;
        },
        updUsuario: async (_, { id, input }) => {
            return await Usuario.findByIdAndUpdate(id, input, { new: true });
        },
        delUsuario: async (_, { id }) => {
            await Usuario.deleteOne ({ _id: id});
            return {message: "Usuario eliminado"};
        }
    }   
};

module.exports = { usuarioTypeDefs, usuarioResolvers };