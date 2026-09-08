const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const { ApolloServer, gql } = require('apollo-server-express');

const {usuarioTypeDefs, UsarioResolvers, usuarioResolvers} = require('./usuarioModule')
const {flavorTypeDefs, FlavorResolvers, flavorResolvers} = require('./flavorModule')

const baseTypeDefs = gql `
    type Query {
        _empty: String
    }
    type Mutation {
        _empty: String
    }
`;

async function startServer() {
    const app = express();

    const corsOptions = {
        origin: '*',
        credentials: false
    };
    app.use(cors(corsOptions));

    mongoose.connect('mongodb://localhost:27017/frio_natural')
        .then(() => console.log('Esta VIVOOOOO (se conecto con MongoDB)'))
        .catch(err => console.error('NOOOOOOOOOO: ', err));
    
    const server = new ApolloServer({
        typeDefs: [baseTypeDefs, usuarioTypeDefs, flavorTypeDefs],
        resolvers: [usuarioResolvers, flavorResolvers]
    });

    await server.start();
    server.applyMiddleware({ app, cors: false});

    app.listen(8090, () => {
        console.log('GraphQL iniciado en http://localhost:8090' + server.graphqlPath);
    });
}

startServer();