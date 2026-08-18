<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Nuestra Empresa</title>
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

        <div class="container mt-5 mb-5 flex-grow-1">
            <div class="row">
                <div class="col-12 text-center mb-4">
                    <h2>Nuestra Empresa</h2>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-6 mb-3">
                    <div class="p-4 bg-warning border rounded h-100">
                        <h3>Quiénes Somos</h3>
                        <p>Somos una empresa dedicada a ofrecer las mejores soluciones para nuestros clientes. Trabajamos con dedicación y compromiso en cada proyecto que emprendemos.</p>
                    </div>
                </div>
                <div class="col-sm-6 mb-3">
                    <div class="p-4 bg-success border rounded h-100">
                        <h3>Nuestra Misión</h3>
                        <p>Nuestra misión es innovar y entregar servicios de alta calidad, asegurando la satisfacción total y construyendo relaciones de confianza a largo plazo.</p>
                    </div>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12">
                    <div class="p-4 bg-info border rounded">
                        <h3>Nuestro Equipo</h3>
                        <p>Contamos con un grupo de profesionales altamente capacitados y dispuestos a dar lo mejor de sí para cumplir con los objetivos trazados.</p>
                    </div>
                </div>
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