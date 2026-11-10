workspace "Frio Natural" "Arquitectura del backend de Frio Natural (Entrega 2)" {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Usuario autenticado (rol user) que consulta productos, crea pedidos y paga."
        administrador = person "Administrador" "Usuario autenticado (roles user y admin) que ademas crea, modifica y elimina productos."

        sistema = softwareSystem "Frio Natural" "Sistema de venta de helados y paletas: autenticacion, catalogo, pedidos, pagos simulados y analitica de ventas." {
            tags "SistemaEvaluado"

            frontend = container "Frontend web" "Pagina simulada de Frio Natural (Semana 7). Aun no esta integrada al backend." "Aplicacion web" {
                tags "Frontend"
            }

            apiGateway = container "API Gateway" "Unico punto de entrada (puerto 8000). Valida la cookie de sesion, autoriza por rol y propaga la identidad al backend." "FastAPI / Python" {
                tags "Gateway"

                // C3 - API Gateway (gateway.py)
                httpEntry = component "Endpoints del Gateway" "Expone /health, /auth/login, /auth/me, /auth/logout, /api/* y /graphql. Maneja la cookie HttpOnly session_token." "FastAPI routes" {
                    tags "EntradaC3"
                }
                sessionValidator = component "Validador de sesion" "get_session: lee la cookie y la valida contra el Auth Service (introspect)." "Funcion de seguridad" {
                    tags "ControlC3"
                }
                vaultClient = component "Cliente de Vault" "get_vault_secrets: obtiene backend_shared_secret y auth_introspection_secret." "Adaptador de integracion" {
                    tags "IntegracionC3"
                }
                roleAuthorizer = component "Autorizacion por rol" "authorize: solo admin puede crear, modificar o eliminar productos (rutas /api)." "Regla de autorizacion" {
                    tags "ControlC3"
                }
                proxyDispatcher = component "Proxy hacia backend y GraphQL" "Construye headers nuevos (X-Gateway-Secret, X-Authenticated-*) y reenvia la peticion." "httpx" {
                    tags "AplicacionC3"
                }
                errorMapper = component "Manejo de errores HTTP" "Devuelve 401, 403, 502 o 503 sin exponer detalles internos." "HTTPException" {
                    tags "ErrorC3"
                }
            }

            authService = container "Auth Service" "Login, introspeccion y logout (puerto 8100). Sesiones de 15 minutos y usuarios guardados en memoria." "FastAPI / Python" {
                tags "Seguridad"

                // C3 - Auth Service (auth_service.py)
                identityApi = component "API de identidad" "Atiende /login, /introspect, /logout y /health." "FastAPI routes" {
                    tags "EntradaC3"
                }
                gatewaySecretCheck = component "Verificador de secreto del Gateway" "verify_gateway_secret: exige X-Gateway-Auth-Secret en introspect y logout." "Control de acceso" {
                    tags "ControlC3"
                }
                credentialsVerifier = component "Verificador de credenciales" "Compara la clave contra el hash PBKDF2 (200000 iteraciones) en tiempo constante." "hashlib / hmac" {
                    tags "ControlC3"
                }
                sessionManager = component "Gestor de sesiones" "Crea tokens aleatorios, controla expiracion (900 s) y revoca en logout." "Diccionario SESSIONS en memoria" {
                    tags "AplicacionC3"
                }
                userStore = component "Almacen de usuarios" "Usuarios, roles y hashes de clave (ana, ernesto, matias, christian)." "Diccionario USERS en memoria" {
                    tags "PersistenciaC3"
                }
            }

            vault = container "Vault" "Guarda los secretos compartidos entre servicios (puerto 8200). vault-init los carga al arrancar." "HashiCorp Vault (modo dev)" {
                tags "Seguridad"
            }

            backendApi = container "Backend API" "Logica de negocio (puerto 9000): productos, pedidos, pagos simulados e informacion de la tienda. Solo acepta llamadas con X-Gateway-Secret." "FastAPI / Python" {
                tags "Privado"

                // C3 - Backend API (backend_api.py + database.py)
                backendEntry = component "Endpoints del backend" "Expone /products, /orders, /payments/{id}, /store-info y /health." "FastAPI routes" {
                    tags "EntradaC3"
                }
                gatewayGuard = component "Verificacion de Gateway e identidad" "verify_gateway, get_identity y require_admin: bloquea el acceso directo y aplica rol admin." "Dependencias FastAPI" {
                    tags "ControlC3"
                }
                productsModule = component "Modulo de productos" "Catalogo y stock (tabla flavors). Escritura solo para admin." "Servicio de aplicacion" {
                    tags "AplicacionC3"
                }
                ordersModule = component "Modulo de pedidos" "Crea pedidos con precios tomados de la BD; un usuario solo ve los suyos, admin ve todos." "Servicio de aplicacion" {
                    tags "AplicacionC3"
                }
                paymentsModule = component "Modulo de pagos (simulado)" "Cambia el pedido a estado pagado; rechaza pagos repetidos con 409." "Servicio de aplicacion" {
                    tags "AplicacionC3"
                }
                analyticsClient = component "Cliente gRPC de analitica" "Llama LogSale tras un pago; si falla, solo registra un aviso." "grpc / analytics_pb2" {
                    tags "IntegracionC3"
                }
                dataAccess = component "Acceso a datos" "database.py: conexiones SQLite, esquema, datos iniciales y lectura de data/*.json." "sqlite3" {
                    tags "PersistenciaC3"
                }
            }

            graphqlService = container "GraphQL Service" "Consulta agregada order_summary (puerto 8050): combina un pedido con los productos de sus lineas." "FastAPI + Strawberry" {
                tags "Privado"

                // C3 - GraphQL Service (graphql_service.py)
                graphqlEndpoint = component "Endpoint GraphQL" "Recibe operaciones en /graphql y arma el contexto de la peticion." "Strawberry GraphQLRouter" {
                    tags "EntradaC3"
                }
                gatewayHeaderCheck = component "Verificacion de acceso" "Exige que venga X-Gateway-Secret; el valor lo valida el Backend API." "Control de acceso" {
                    tags "ControlC3"
                }
                orderSummaryResolver = component "Resolver order_summary" "Obtiene el pedido y el producto de cada linea y compone OrderSummary." "Resolver GraphQL" {
                    tags "AplicacionC3"
                }
                backendConnector = component "Conector al Backend API" "Cliente HTTP hacia /orders/{id} y /products/{id} reenviando secreto e identidad." "httpx" {
                    tags "IntegracionC3"
                }
            }

            analyticsService = container "Analytics Service" "Registra ventas pagadas (puerto 50051) mediante la operacion gRPC LogSale." "Python gRPC" {
                tags "Analitica"
            }

            dbFrioNatural = container "Base de datos frio_natural.db" "Tablas flavors, pedidos y detalle_pedido. Persiste en el volumen backend-data." "SQLite" {
                tags "BaseDatos"
            }
        }

        // ---------- C1: contexto ----------
        cliente -> sistema "Consulta productos, crea pedidos y paga"
        administrador -> sistema "Administra el catalogo de productos"

        // ---------- C2: relaciones entre contenedores ----------
        cliente -> sistema.frontend "Usa la tienda" "Navegador web"
        administrador -> sistema.frontend "Administra productos" "Navegador web"
        sistema.frontend -> sistema.apiGateway "Envia solicitudes con cookie de sesion" "HTTP (HTTPS en produccion)"
        sistema.apiGateway -> sistema.authService "Login, introspeccion y logout" "HTTP/JSON"
        sistema.apiGateway -> sistema.vault "Lee secretos del Gateway" "HTTP (X-Vault-Token)"
        sistema.apiGateway -> sistema.backendApi "Enruta /api/* con identidad propagada" "HTTP/JSON"
        sistema.apiGateway -> sistema.graphqlService "Enruta /graphql con identidad propagada" "HTTP/GraphQL"
        sistema.graphqlService -> sistema.backendApi "Consulta pedidos y productos" "HTTP/JSON"
        sistema.backendApi -> sistema.dbFrioNatural "Lee y escribe productos y pedidos" "SQLite"
        sistema.backendApi -> sistema.analyticsService "Notifica venta pagada (LogSale)" "gRPC"

        // Respuestas explicitas (para las vistas dinamicas)
        sistema.authService -> sistema.apiGateway "Responde login, sesion activa o inactiva" "HTTP/JSON"
        sistema.vault -> sistema.apiGateway "Entrega secretos" "HTTP/JSON"
        sistema.backendApi -> sistema.apiGateway "Responde operaciones del backend" "HTTP/JSON"
        sistema.graphqlService -> sistema.apiGateway "Devuelve resultado GraphQL" "HTTP/GraphQL"
        sistema.apiGateway -> sistema.frontend "Devuelve respuestas y errores controlados" "HTTP"
        sistema.frontend -> cliente "Presenta resultados y errores" "Interfaz web"
        sistema.frontend -> administrador "Presenta resultados y errores" "Interfaz web"
        sistema.backendApi -> sistema.graphqlService "Devuelve pedido y productos" "HTTP/JSON"
        sistema.dbFrioNatural -> sistema.backendApi "Devuelve datos y confirma escrituras" "SQLite"
        sistema.analyticsService -> sistema.backendApi "Confirma registro de venta" "gRPC"

        // ---------- C3: API Gateway ----------
        sistema.frontend -> sistema.apiGateway.httpEntry "Invoca funciones del backend" "HTTP"
        sistema.apiGateway.httpEntry -> sistema.authService "Envia login y logout" "HTTP/JSON"
        sistema.apiGateway.httpEntry -> sistema.apiGateway.sessionValidator "Solicita validar la cookie de sesion"
        sistema.apiGateway.sessionValidator -> sistema.apiGateway.vaultClient "Pide el secreto de introspeccion"
        sistema.apiGateway.vaultClient -> sistema.vault "Lee secretos" "HTTP (X-Vault-Token)"
        sistema.apiGateway.sessionValidator -> sistema.authService "Introspecciona el token" "HTTP/JSON"
        sistema.apiGateway.sessionValidator -> sistema.apiGateway.roleAuthorizer "Entrega identidad y roles (rutas /api)"
        sistema.apiGateway.sessionValidator -> sistema.apiGateway.proxyDispatcher "Entrega identidad (ruta /graphql)"
        sistema.apiGateway.sessionValidator -> sistema.apiGateway.errorMapper "Reporta sesion ausente o invalida (401)"
        sistema.apiGateway.roleAuthorizer -> sistema.apiGateway.proxyDispatcher "Permite la operacion"
        sistema.apiGateway.roleAuthorizer -> sistema.apiGateway.errorMapper "Reporta rol insuficiente (403)"
        sistema.apiGateway.proxyDispatcher -> sistema.backendApi "Reenvia /api/*" "HTTP/JSON"
        sistema.apiGateway.proxyDispatcher -> sistema.graphqlService "Reenvia /graphql" "HTTP/GraphQL"
        sistema.apiGateway.proxyDispatcher -> sistema.apiGateway.errorMapper "Reporta servicio no disponible (502)"

        // ---------- C3: Auth Service ----------
        sistema.apiGateway -> sistema.authService.identityApi "Login, introspeccion y logout" "HTTP/JSON"
        sistema.authService.identityApi -> sistema.authService.gatewaySecretCheck "Verifica secreto en introspect y logout"
        sistema.authService.identityApi -> sistema.authService.credentialsVerifier "Verifica credenciales en login"
        sistema.authService.credentialsVerifier -> sistema.authService.userStore "Consulta usuario y hash"
        sistema.authService.identityApi -> sistema.authService.sessionManager "Crea, consulta y revoca sesiones"

        // ---------- C3: Backend API ----------
        sistema.apiGateway -> sistema.backendApi.backendEntry "Enruta /api/*" "HTTP/JSON"
        sistema.graphqlService -> sistema.backendApi.backendEntry "Consulta pedidos y productos" "HTTP/JSON"
        sistema.backendApi.backendEntry -> sistema.backendApi.gatewayGuard "Verifica secreto e identidad"
        sistema.backendApi.gatewayGuard -> sistema.backendApi.productsModule "Permite operaciones de productos"
        sistema.backendApi.gatewayGuard -> sistema.backendApi.ordersModule "Permite operaciones de pedidos"
        sistema.backendApi.gatewayGuard -> sistema.backendApi.paymentsModule "Permite operaciones de pago"
        sistema.backendApi.productsModule -> sistema.backendApi.dataAccess "Lee y escribe flavors"
        sistema.backendApi.ordersModule -> sistema.backendApi.dataAccess "Lee y escribe pedidos y detalle"
        sistema.backendApi.paymentsModule -> sistema.backendApi.dataAccess "Actualiza estado del pedido"
        sistema.backendApi.paymentsModule -> sistema.backendApi.analyticsClient "Solicita registrar la venta"
        sistema.backendApi.analyticsClient -> sistema.analyticsService "Invoca LogSale" "gRPC"
        sistema.backendApi.dataAccess -> sistema.dbFrioNatural "Accede a la base" "SQLite"

        // ---------- C3: GraphQL Service ----------
        sistema.apiGateway -> sistema.graphqlService.graphqlEndpoint "Remite operaciones GraphQL" "HTTP/GraphQL"
        sistema.graphqlService.graphqlEndpoint -> sistema.graphqlService.gatewayHeaderCheck "Verifica cabecera del Gateway"
        sistema.graphqlService.gatewayHeaderCheck -> sistema.graphqlService.orderSummaryResolver "Permite la consulta"
        sistema.graphqlService.orderSummaryResolver -> sistema.graphqlService.backendConnector "Solicita pedido y productos"
        sistema.graphqlService.backendConnector -> sistema.backendApi "Consulta /orders/id y /products/id" "HTTP/JSON"

        // ---------- DESPLIEGUE: Docker Compose (docker-compose.yml) ----------
        desarrollo = deploymentEnvironment "Docker_Compose" {
            deploymentNode "Equipo del usuario" "Equipo con navegador web." "Equipo cliente" {
                tags "ZonaCliente"
                deploymentNode "Navegador web" "Ejecuta el frontend; no es un servidor." "Navegador" {
                    containerInstance sistema.frontend
                }
            }
            deploymentNode "Equipo de desarrollo" "Maquina que ejecuta docker compose up --build. Todos los servicios publican su puerto en el host." "Docker Compose" {
                tags "ZonaLocal"
                deploymentNode "api-gateway" "Contenedor; puerto 8000:8000." "Docker (uvicorn gateway:app)" {
                    tags "ZonaPublica"
                    containerInstance sistema.apiGateway
                }
                deploymentNode "auth-service" "Contenedor; puerto 8100:8100." "Docker (uvicorn auth_service:app)" {
                    tags "ZonaPrivada"
                    containerInstance sistema.authService
                }
                deploymentNode "backend-api" "Contenedor; puerto 9000:9000; monta el volumen backend-data en /data." "Docker (uvicorn backend_api:app)" {
                    tags "ZonaPrivada"
                    containerInstance sistema.backendApi
                }
                deploymentNode "graphql-service" "Contenedor; puerto 8050." "Docker (uvicorn graphql_service:app)" {
                    tags "ZonaPrivada"
                    containerInstance sistema.graphqlService
                }
                deploymentNode "analytics-service" "Contenedor; puerto gRPC 50051." "Docker (python analytics_service.py)" {
                    tags "ZonaPrivada"
                    containerInstance sistema.analyticsService
                }
                deploymentNode "vault-dev" "Contenedor; puerto 8200:8200. vault-init carga los secretos y termina." "Docker (hashicorp/vault)" {
                    tags "ZonaSecretos"
                    containerInstance sistema.vault
                }
                deploymentNode "Volumen backend-data" "Volumen Docker montado en /data de backend-api." "Docker volume" {
                    tags "ZonaDatos"
                    containerInstance sistema.dbFrioNatural
                }
            }
        }
    }

    views {
        systemContext sistema "C1_Contexto" "Actores y sistema Frio Natural." {
            title "C1 - Contexto de Frio Natural"
            include *
            autoLayout lr
        }

        container sistema "C2_Contenedores" "Servicios y base de datos de Frio Natural." {
            title "C2 - Contenedores de Frio Natural"
            include *
            autoLayout lr
        }

        container sistema "C2_Pedidos_Pagos" "Recorrido estructural de pedidos y pagos." {
            title "C2 - Pedidos y pagos"
            include cliente sistema.frontend sistema.apiGateway sistema.authService sistema.vault sistema.backendApi sistema.dbFrioNatural sistema.analyticsService
            autoLayout lr
        }

        component sistema.apiGateway "C3_API_Gateway" "Componentes internos del API Gateway." {
            title "C3 - API Gateway"
            include *
            autoLayout lr
        }

        component sistema.authService "C3_Auth_Service" "Identidad, sesiones y credenciales." {
            title "C3 - Auth Service"
            include *
            autoLayout lr
        }

        component sistema.backendApi "C3_Backend_API" "Productos, pedidos, pagos y persistencia." {
            title "C3 - Backend API"
            include *
            autoLayout lr
        }

        component sistema.graphqlService "C3_GraphQL" "Consulta agregada de pedido y productos." {
            title "C3 - GraphQL Service"
            include *
            autoLayout lr
        }

        // ---------- Vistas dinamicas ----------
        dynamic sistema "D_Login" "Inicio de sesion: el token viaja solo en cookie HttpOnly." {
            title "Login exitoso"
            1: cliente -> sistema.frontend "Ingresa usuario y clave"
            2: sistema.frontend -> sistema.apiGateway "POST /auth/login" "HTTP"
            3: sistema.apiGateway -> sistema.authService "POST /login" "HTTP/JSON"
            4: sistema.authService -> sistema.apiGateway "Devuelve access_token (15 min)" "HTTP/JSON"
            5: sistema.apiGateway -> sistema.frontend "200 y cookie session_token HttpOnly" "HTTP"
            6: sistema.frontend -> cliente "Muestra sesion iniciada"
            autoLayout lr
        }

        dynamic sistema "D_Crear_Pedido" "Creacion de pedido con sesion valida; el precio sale de la base de datos." {
            title "Crear pedido: exito"
            1: cliente -> sistema.frontend "Confirma el carrito"
            2: sistema.frontend -> sistema.apiGateway "POST /api/orders con cookie" "HTTP"
            3: sistema.apiGateway -> sistema.vault "Lee secretos del Gateway" "HTTP"
            4: sistema.vault -> sistema.apiGateway "Entrega secretos" "HTTP/JSON"
            5: sistema.apiGateway -> sistema.authService "POST /introspect" "HTTP/JSON"
            6: sistema.authService -> sistema.apiGateway "Sesion activa con user_id y roles" "HTTP/JSON"
            7: sistema.apiGateway -> sistema.backendApi "POST /orders con X-Gateway-Secret e identidad" "HTTP/JSON"
            8: sistema.backendApi -> sistema.dbFrioNatural "Lee precios; inserta pedido y detalle" "SQLite"
            9: sistema.dbFrioNatural -> sistema.backendApi "Confirma escritura" "SQLite"
            10: sistema.backendApi -> sistema.apiGateway "201 con pedido en estado pendiente" "HTTP/JSON"
            11: sistema.apiGateway -> sistema.frontend "Devuelve el pedido" "HTTP"
            12: sistema.frontend -> cliente "Muestra el pedido creado"
            autoLayout lr
        }

        dynamic sistema "D_Pago" "Pago simulado: cambia el estado y notifica a analitica por gRPC." {
            title "Pago de pedido y registro de venta"
            1: cliente -> sistema.frontend "Paga un pedido propio"
            2: sistema.frontend -> sistema.apiGateway "POST /api/payments/id" "HTTP"
            3: sistema.apiGateway -> sistema.authService "Valida sesion (introspect)" "HTTP/JSON"
            4: sistema.authService -> sistema.apiGateway "Sesion activa" "HTTP/JSON"
            5: sistema.apiGateway -> sistema.backendApi "POST /payments/id" "HTTP/JSON"
            6: sistema.backendApi -> sistema.dbFrioNatural "Actualiza estado a pagado" "SQLite"
            7: sistema.dbFrioNatural -> sistema.backendApi "Confirma actualizacion" "SQLite"
            8: sistema.backendApi -> sistema.analyticsService "LogSale(order_id, total)" "gRPC"
            9: sistema.analyticsService -> sistema.backendApi "SaleResponse(success)" "gRPC"
            10: sistema.backendApi -> sistema.apiGateway "Pago procesado" "HTTP/JSON"
            11: sistema.apiGateway -> sistema.frontend "Devuelve pedido pagado" "HTTP"
            12: sistema.frontend -> cliente "Muestra pago exitoso"
            autoLayout lr
        }

        dynamic sistema "D_Acceso_Denegado" "Un usuario sin rol admin intenta eliminar un producto: el Gateway lo rechaza." {
            title "Rechazo por rol insuficiente (403)"
            1: cliente -> sistema.frontend "Intenta eliminar un producto"
            2: sistema.frontend -> sistema.apiGateway "DELETE /api/products/id" "HTTP"
            3: sistema.apiGateway -> sistema.authService "Valida sesion (introspect)" "HTTP/JSON"
            4: sistema.authService -> sistema.apiGateway "Sesion activa con rol user" "HTTP/JSON"
            5: sistema.apiGateway -> sistema.frontend "403: se requiere rol administrador (no llega al backend)" "HTTP"
            6: sistema.frontend -> cliente "Muestra el rechazo"
            autoLayout lr
        }

        dynamic sistema "D_Backend_Caido" "El Gateway devuelve un error controlado si el backend no responde." {
            title "Fallo controlado: backend no disponible (502)"
            1: cliente -> sistema.frontend "Abre el catalogo"
            2: sistema.frontend -> sistema.apiGateway "GET /api/products" "HTTP"
            3: sistema.apiGateway -> sistema.authService "Valida sesion (introspect)" "HTTP/JSON"
            4: sistema.authService -> sistema.apiGateway "Sesion activa" "HTTP/JSON"
            5: sistema.apiGateway -> sistema.backendApi "Reenvia consulta; el backend no responde" "HTTP/JSON"
            6: sistema.apiGateway -> sistema.frontend "502: Backend no disponible" "HTTP"
            7: sistema.frontend -> cliente "Muestra error sin datos falsos"
            autoLayout lr
        }

        dynamic sistema "D_GraphQL_Pedido" "Consulta agregada: pedido mas producto de cada linea." {
            title "GraphQL: resumen de pedido"
            1: cliente -> sistema.frontend "Consulta resumen de un pedido"
            2: sistema.frontend -> sistema.apiGateway "POST /graphql" "HTTP"
            3: sistema.apiGateway -> sistema.authService "Valida sesion (introspect)" "HTTP/JSON"
            4: sistema.authService -> sistema.apiGateway "Sesion activa" "HTTP/JSON"
            5: sistema.apiGateway -> sistema.graphqlService "Reenvia consulta con secreto e identidad" "HTTP/GraphQL"
            6: sistema.graphqlService -> sistema.backendApi "GET /orders/id" "HTTP/JSON"
            7: sistema.backendApi -> sistema.graphqlService "Devuelve el pedido" "HTTP/JSON"
            8: sistema.graphqlService -> sistema.backendApi "GET /products/id por cada linea" "HTTP/JSON"
            9: sistema.backendApi -> sistema.graphqlService "Devuelve los productos" "HTTP/JSON"
            10: sistema.graphqlService -> sistema.apiGateway "Devuelve OrderSummary" "HTTP/GraphQL"
            11: sistema.apiGateway -> sistema.frontend "Entrega resultado" "HTTP"
            12: sistema.frontend -> cliente "Muestra el resumen"
            autoLayout lr
        }

        // ---------- Vista de despliegue ----------
        deployment sistema desarrollo "DEP_Docker_Compose" "Servicios de docker-compose.yml en un equipo de desarrollo." {
            title "Despliegue - Docker Compose"
            include *
            autoLayout lr
        }

        styles {
            element "Deployment Node" {
                background #E9EFF5
                color #213F56
                stroke #8FA5B7
            }
            element "Infrastructure Node" {
                shape roundedbox
                background #EDF0F3
                color #334454
            }
            element "ZonaCliente" {
                background #F1F5F9
                color #173B5D
            }
            element "ZonaPublica" {
                background #DCEAF7
                color #173B5D
            }
            element "ZonaPrivada" {
                background #E5EEE8
                color #20513D
            }
            element "ZonaDatos" {
                background #ECEAF2
                color #463D64
            }
            element "ZonaSecretos" {
                background #EEE5E1
                color #68483C
            }
            element "ZonaLocal" {
                background #F0F3F6
                color #243F56
            }
            element "Person" {
                shape person
                background #56718A
                color #FFFFFF
            }
            element "Software System" {
                shape roundedbox
                background #0C527A
                color #FFFFFF
            }
            element "SistemaEvaluado" {
                background #173B5D
                color #FFFFFF
            }
            element "Container" {
                shape roundedbox
                background #E3ECF5
                color #173B5D
            }
            element "Frontend" {
                shape webbrowser
                background #CDE5F7
                color #153E5B
            }
            element "Gateway" {
                background #2B6289
                color #FFFFFF
            }
            element "Seguridad" {
                background #3F6171
                color #FFFFFF
            }
            element "Privado" {
                background #D5E8EF
                color #173B5D
            }
            element "BaseDatos" {
                shape cylinder
                background #E5EAF0
                color #243F56
            }
            element "Analitica" {
                background #E7E0F2
                color #453166
            }
            element "Component" {
                shape roundedbox
                background #EDF3F7
                color #173B5D
            }
            element "EntradaC3" {
                background #D3E9F7
                color #153F62
            }
            element "ControlC3" {
                background #DBE4EC
                color #213F56
            }
            element "AplicacionC3" {
                background #D7E9DE
                color #20533E
            }
            element "IntegracionC3" {
                background #E9E2F2
                color #4A3666
            }
            element "PersistenciaC3" {
                background #E9EBEE
                color #334454
            }
            element "ErrorC3" {
                background #F2E6DB
                color #70462C
            }
            relationship "Relationship" {
                color #60758A
                thickness 2
            }
        }
    }
}
