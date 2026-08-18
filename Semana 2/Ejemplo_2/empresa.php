<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Empresa</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>

  <!-- NAVBAR -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="index.php">Logo</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">Empresa</a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="empresa.php">Quiénes somos</a></li>
              <li><a class="dropdown-item" href="empresa.php">Nuestro equipo</a></li>
              <li><a class="dropdown-item" href="empresa.php">Misión</a></li>
            </ul>
          </li>
          <li class="nav-item"><a class="nav-link" href="productos.php">Productos</a></li>
          <li class="nav-item"><a class="nav-link" href="servicios.php">Servicios</a></li>
          <li class="nav-item"><a class="nav-link" href="contacto.php">Contacto</a></li>
        </ul>
      </div>
      <!-- Botón login -->
      <button class="btn btn-outline-light" data-bs-toggle="modal" data-bs-target="#myModal">
        Acceder <i class="fa fa-check-circle"></i>
      </button>
    </div>
  </nav>

  <!-- CONTENIDO -->
  <div class="container mt-4">
    <h1>Empresa</h1>
    <p>Quiénes somos, nuestro equipo y nuestra misión.</p>
  </div>

  <!-- FOOTER -->
  <div class="container-fluid bg-dark mt-5">
    <div class="row d-flex justify-content-center">
      <div class="col-4 text-center py-2">
        <strong style="color:white">Mi Empresa @ 2026</strong>
      </div>
    </div>
  </div>

  <!-- MODAL LOGIN -->
  <div class="modal fade" id="myModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Iniciar sesión</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <form action="empresa.php">
            <div class="mb-2">
              <label>Email</label>
              <input type="email" class="form-control">
            </div>
            <div class="mb-2">
              <label>Password</label>
              <input type="password" class="form-control">
            </div>
            <div class="form-check mb-2">
              <input type="checkbox" class="form-check-input">
              <label class="form-check-label">Recordarme</label>
            </div>
            <button type="submit" class="btn btn-primary mt-1">Login</button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
