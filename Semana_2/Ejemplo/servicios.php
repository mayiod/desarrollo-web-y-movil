<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Nuestros Servicios</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>        
    </head>
    <body class="d-flex flex-column min-vh-100">
        
        <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="index.php">
                    <img class="bg-light rounded p-2" width="50" src="img/guitarra.png" alt="Logo Guitarra">
                </a>  
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
                <span class="navbar-toggler-icon"></span>
                </button>        
                <div class="collapse navbar-collapse" id="collapsibleNavbar">        
                    <ul class="navbar-nav">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Empresa</a>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="empresa.php">Quienes Somos</a></li>
                                <li><a class="dropdown-item" href="#">Nuestro Equipo</a></li>
                                <li><a class="dropdown-item" href="#">Mision</a></li>
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
                </div> 
                <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#myModal">Acceder</button>             
            </div>         
        </nav>
        
        <div class="container mt-4 mb-4 flex-grow-1">
            
            <div class="row mb-4">
                <div class="col-12 text-center">
                    <h2>Nuestros Servicios</h2>
                </div>
            </div>

            <div id="demo" class="carousel slide mb-5" data-bs-ride="carousel">
                <div class="carousel-indicators">
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="0" class="active"></button>
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="1"></button>
                    <button type="button" data-bs-target="#demo" data-bs-slide-to="2"></button>
                </div>
                <div class="carousel-inner">
                    <div class="carousel-item active">
                        <img src="img/la.jpg" alt="Concierto" class="d-block w-100 img-fluid">
                    </div>
                    <div class="carousel-item">
                        <img src="img/chicago.jpg" alt="Estudio de Grabación" class="d-block w-100 img-fluid">
                    </div>
                    <div class="carousel-item">
                        <img src="img/ny.jpg" alt="Instrumentos Musicales" class="d-block w-100 img-fluid">
                    </div>
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#demo" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon"></span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#demo" data-bs-slide="next">
                    <span class="carousel-control-next-icon"></span>
                </button>
            </div>

            <div class="row text-center mb-4">
                <div class="col-sm-4 mb-3">
                    <div class="p-3 bg-light border rounded h-100">
                        <h4>Arriendo de Instrumentos</h4>
                        <p>Teclados, guitarras, bajos y baterías disponibles para tus ensayos o eventos.</p>
                        <button class="btn btn-primary mt-2">Cotizar arriendo</button>
                    </div>
                </div>
                <div class="col-sm-4 mb-3">
                    <div class="p-3 bg-light border rounded h-100">
                        <h4>Presentaciones en Vivo</h4>
                        <p>Músicos profesionales y bandas completas para amenizar cualquier tipo de celebración.</p>
                        <button class="btn btn-primary mt-2">Ver catálogo</button>
                    </div>
                </div>
                <div class="col-sm-4 mb-3">
                    <div class="p-3 bg-light border rounded h-100">
                        <h4>Sonido e Iluminación</h4>
                        <p>Equipamiento técnico completo para asegurar la mejor calidad de audio en tus eventos.</p>
                        <button class="btn btn-primary mt-2">Más información</button>
                    </div>
                </div>
            </div>

            <div class="d-flex justify-content-center">
                <ul class="pagination">
                    <li class="page-item"><a class="page-link" href="#">Anterior</a></li>
                    <li class="page-item active"><a class="page-link" href="#">1</a></li>
                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                    <li class="page-item"><a class="page-link" href="#">3</a></li>
                    <li class="page-item"><a class="page-link" href="#">Siguiente</a></li>
                </ul>
            </div>
            
        </div>
        
        <div class="container-fluid bg-dark mt-auto">
            <div class="row d-flex justify-content-center">
                <div class="col-4 text-center">
                    <strong style="color:white">MiEmpresa@2026</strong>
                </div>
            </div>
        </div>
        
        <div class="modal fade" id="myModal">
            <div class="modal-dialog">
                <div class="modal-content">
                    
                    <div class="modal-header">
                        <h4 class="modal-title">Autenticación</h4>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    
                    <div class="modal-body">
                        <form action="empresa.php">
                            <div class="mb-3 mt-3">
                                <label for="email" class="form-label">Email:</label>
                                <input type="email" class="form-control" id="email" placeholder="Enter email" name="email">
                            </div>
                            <div class="mb-3">
                                <label for="pwd" class="form-label">Password:</label>
                                <input type="password" class="form-control" id="pwd" placeholder="Enter password" name="pswd">
                            </div>
                            <div class="form-check mb-3">
                                <label class="form-check-label">
                                    <input class="form-check-input" type="checkbox" name="remember"> Remember me
                                </label>
                            </div>
                            <button type="submit" class="btn btn-primary">Login</button>
                        </form>
                    </div>
                    
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>         
    </body>
</html>