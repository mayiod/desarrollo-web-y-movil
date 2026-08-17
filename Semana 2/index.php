<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Foro de Discusión - Comunidad Tech</title>
    
    <!-- Bootstrap 5 CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
    
    <style>
        body {
            background-color: #f4f6f9;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .main-container {
            flex: 1;
        }
        .category-card {
            transition: transform 0.2s;
        }
        .category-card:hover {
            transform: translateY(-2px);
        }
    </style>
</head>
<body>

    <!-- ================= NAVBAR ================= -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
        <div class="container">
            <a class="navbar-brand fw-bold" href="index.php">
                <span class="text-primary">Dev</span>Foro
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarForo">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarForo">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" href="index.php">Inicio</a>
                    </li>
                    
                    <!-- Dropdown de Categorías de Empresa / Secciones -->
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                            Categorías
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="empresa.php">Comunidad & Empresa</a></li>
                            <li><a class="dropdown-item" href="productos.php">Proyectos & Productos</a></li>
                            <li><a class="dropdown-item" href="servicios.php">Servicios & Empleos</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="contacto.php">Soporte y Contacto</a></li>
                        </ul>
                    </li>
                    
                    <li class="nav-item">
                        <a class="nav-link" href="productos.php">Productos</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="servicios.php">Servicios</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="contacto.php">Contacto</a>
                    </li>
                </ul>

                <!-- Botón que activa el Modal de Login -->
                <button type="button" class="btn btn-outline-light" data-bs-toggle="modal" data-bs-target="#modalLogin">
                    Acceder
                </button>
            </div>
        </div>
    </nav>

    <!-- ================= CONTENIDO PRINCIPAL ================= -->
    <div class="container main-container my-4">

        <!-- CARRUSEL RESPONSIVO (Anuncios / Temas Destacados) -->
        <div id="carruselDestacados" class="carousel slide shadow-sm rounded overflow-hidden mb-4" data-bs-ride="carousel">
            <div class="carousel-indicators">
                <button type="button" data-bs-target="#carruselDestacados" data-bs-slide-to="0" class="active"></button>
                <button type="button" data-bs-target="#carruselDestacados" data-bs-slide-to="1"></button>
                <button type="button" data-bs-target="#carruselDestacados" data-bs-slide-to="2"></button>
            </div>
            
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <img src="https://via.placeholder.com/1200x300/2c3e50/ffffff?text=Reglas+de+la+Comunidad+y+Bienvenida" class="d-block w-100" alt="Reglas del foro">
                    <div class="carousel-caption d-none d-md-block">
                        <h5>¡Bienvenido a la comunidad!</h5>
                        <p>Lee las normas antes de publicar un nuevo tema.</p>
                    </div>
                </div>
                <div class="carousel-item">
                    <img src="https://via.placeholder.com/1200x300/16a085/ffffff?text=Debate+Semanal:+Desarrollo+Web+y+PHP" class="d-block w-100" alt="Debate PHP">
                    <div class="carousel-caption d-none d-md-block">
                        <h5>Debate Semanal</h5>
                        <p>Aprende las mejores prácticas para estructurar tus proyectos Web.</p>
                    </div>
                </div>
                <div class="carousel-item">
                    <img src="https://via.placeholder.com/1200x300/2980b9/ffffff?text=Hackathon+2026:+Presenta+tu+Proyecto" class="d-block w-100" alt="Hackathon">
                    <div class="carousel-caption d-none d-md-block">
                        <h5>Concursos & Eventos</h5>
                        <p>Participa y comparte tus desarrollos con otros compañeros.</p>
                    </div>
                </div>
            </div>

            <button class="carousel-control-prev" type="button" data-bs-target="#carruselDestacados" data-bs-slide="prev">
                <span class="carousel-control-prev-icon"></span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carruselDestacados" data-bs-slide="next">
                <span class="carousel-control-next-icon"></span>
            </button>
        </div>

        <!-- SALAS / CATEGORÍAS DEL FORO -->
        <div class="row g-4">
            
            <!-- Columna Principal: Salas de Texto -->
            <div class="col-lg-8">
                <h4 class="fw-bold mb-3">Salas de Discusión</h4>

                <!-- Categoria 1 -->
                <div class="card mb-3 shadow-sm category-card border-0">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge bg-primary">General</span>
                            <small class="text-muted">0 Mensajes</small>
                        </div>
                        <h5 class="card-title"><a href="#" class="text-decoration-none text-dark fw-bold"> Anuncios Generales</a></h5>
                        <p class="card-text text-muted">Notificaciones oficiales, actualizaciones del sitio y reglamentos.</p>
                    </div>
                </div>

                <!-- Categoria 2 -->
                <div class="card mb-3 shadow-sm category-card border-0">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge bg-success">Desarrollo</span>
                            <small class="text-muted">0 Mensajes</small>
                        </div>
                        <h5 class="card-title"><a href="#" class="text-decoration-none text-dark fw-bold"> Programación & Frontend</a></h5>
                        <p class="card-text text-muted">Discusiones sobre HTML, CSS, JavaScript, Bootstrap y frameworks.</p>
                    </div>
                </div>

                <!-- Categoria 3 -->
                <div class="card mb-3 shadow-sm category-card border-0">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge bg-warning text-dark">PHP & Backend</span>
                            <small class="text-muted">0 Mensajes</small>
                        </div>
                        <h5 class="card-title"><a href="#" class="text-decoration-none text-dark fw-bold"> PHP y Bases de Datos</a></h5>
                        <p class="card-text text-muted">Consultas de MySQL, manejo de sesiones y arquitectura Backend.</p>
                    </div>
                </div>

                <!-- Categoria 4 -->
                <div class="card mb-3 shadow-sm category-card border-0">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge bg-info text-dark">Soporte</span>
                            <small class="text-muted">0 Mensajes</small>
                        </div>
                        <h5 class="card-title"><a href="#" class="text-decoration-none text-dark fw-bold"> Ayuda & Dudas de Clase</a></h5>
                        <p class="card-text text-muted">Espacio para resolver dudas sobre tareas, ejercicios y proyectos.</p>
                    </div>
                </div>
            </div>

            <!-- Columna Lateral: Formulario de Contacto / Mensaje Rápido -->
            <div class="col-lg-4">
                <div class="card shadow-sm border-0 mb-4">
                    <div class="card-header bg-dark text-white fw-bold">
                        🐱 Imagen del día
                    </div>
                    <div class="card-body text-center p-3">
                        <img src="https://cataas.com/cat?width=300&height=300" class="img-fluid rounded shadow-sm" alt="Gato aleatorio">
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- ================= FOOTER ================= -->
    <footer class="bg-dark text-white py-3 border-top mt-auto">
        <div class="container text-center">
            <small><strong>MiEmpresa@2026</strong> — Todos los derechos reservados</small>
        </div>
    </footer>

    <!-- ================= MODAL DE AUTENTICACIÓN / LOGIN ================= -->
    <div class="modal fade" id="modalLogin" tabindex="-1" aria-labelledby="modalLoginLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title" id="modalLoginLabel">Autenticación</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-4">
                    <form action="empresa.php" method="POST">
                        <div class="mb-3">
                            <label for="loginEmail" class="form-label">Correo electrónico:</label>
                            <input type="email" class="form-control" id="loginEmail" name="email" placeholder="ejemplo@correo.com" required>
                        </div>
                        <div class="mb-3">
                            <label for="pwd" class="form-label">Contraseña:</label>
                            <input type="password" class="form-control" id="pwd" name="pswd" placeholder="******" required>
                        </div>
                        <div class="form-check mb-3">
                            <input class="form-check-input" type="checkbox" name="remember" id="remember">
                            <label class="form-check-label" for="remember">
                                Recordarme en este equipo
                            </label>
                        </div>
                        <button type="submit" class="btn btn-primary w-100 fw-bold">Login</button>
                    </form>
                </div>
                <div class="modal-footer bg-light">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cerrar</button>
                </div>
            </div>
        </div>
    </div>

</body>
</html>