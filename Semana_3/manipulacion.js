// 1. Manipulacion de objetos

const registroActividad = {
    contexto_1: { id: 1, estado: "Checkeado", verificado: true},
    contexto_2: { id: 2, estado: "Esperando", verificado: false},
    contexto_borrador: { id: 99, estado: "Borrador", verificado: false}
};

// Recorrer entradas con Object.entries()

console.log("--- Registro inicial del contexto ---");
for (const[clave, valor] of Object.entries(registroActividad)){
    console.log(`Clave: ${clave} / ID: ${valor.id} / Estado: ${valor.estado}`);
}

// Borrar propiedades del objeto con 'delete'

delete registroActividad.contexto_borrador;
console.log("--- Objeto despues dee utilizar 'delete' ---", registroActividad);

/// 2. Modificacion y eventos del DOM

window.addEventListener('DOMContentLoaded', () =>{
    setTimeout(() => {
        const contenedor = document.querySelector('.col-lg-8');
        if(!contenedor) return;

        // Eventos y Actualizacion de estados (DOM)
        contenedor.addEventListener('click', (evento) =>{

            if (evento.target.closest('.btn-votar')){
                const boton = evento.target.closest('.btn-votar');
                const spanVotos = boton.querySelector('span');

                let votosActuales = parseInt(spanVotos.textContent);
                spanVotos.textContent = votosActuales + 1;

                boton.classList.remove('btn-outline-success');
                boton.classList.add('btn-success');

                console.log("Se actualizo el estado, voto registrado en el DOM");
                        
                // Eliminar elementos del DOm

                if (votosActuales > 9){

                    const tarjetaEliminar = boton.closest('.tarjeta-dinamica');
                    
                    if(tarjetaEliminar){
                        tarjetaEliminar.remove();
                        console.log("Elemento eliminado del DOM")
                }}
            }
        });

    }, 500);
});