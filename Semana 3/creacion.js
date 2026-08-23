// 1. Simulación de datos de una API 
const respuestaAPI = {
    status: 200,
    mensaje: "Temas obtenidos correctamente",
    data: [
        { id: 1, titulo: "Dudas con JavaScript y el DOM", categoria: "Soporte", autor: "mayiod" },
        { id: 2, titulo: "Mejores prácticas con Bootstrap 5", categoria: "Desarrollo", autor: "mayiod" }
    ]
};

// 2. Función para crear elementos dinámicamente en runtime
function generarTemasDinamicos() {
    // Buscamos el contenedor principal en el HTML de Bootstrap
    const contenedorSalas = document.querySelector('.col-lg-8');

    if (!contenedorSalas) return;

    // Recorremos los datos simulados
    respuestaAPI.data.forEach(item => {
        // A. Crear el elemento HTML principal usando document.createElement
        const tarjetaDiv = document.createElement('div');
        
        // B. Asignar clases de Bootstrap mediante código (.className o classList)
        tarjetaDiv.className = 'card mb-3 shadow-sm category-card border-0 tarjeta-dinamica';

        // C. Rellenar la estructura interna con innerHTML
        tarjetaDiv.innerHTML = `
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="badge bg-primary">${item.categoria}</span>
                    <small class="text-muted">Autor: ${item.autor}</small>
                </div>
                <h5 class="card-title">
                    <a href="#" class="text-decoration-none text-dark fw-bold">${item.titulo}</a>
                </h5>
                <button class="btn btn-outline-success btn-sm mt-2 btn-votar">Me gusta (<span>0</span>)</button>
            </div>
        `;

        // D. Agregar el elemento creado como hijo usando appendChild 
        contenedorSalas.appendChild(tarjetaDiv);
    });
}

// Ejecutar la función al cargar la página
window.addEventListener('DOMContentLoaded', generarTemasDinamicos);