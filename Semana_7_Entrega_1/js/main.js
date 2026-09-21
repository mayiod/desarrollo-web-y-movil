// Atrapamos los botones de los íconos
const loginBtn = document.getElementById('login-btn');
const cartBtn = document.getElementById('cart-btn');
const searchBtn = document.getElementById('search-btn');

// Atrapamos las ventanas ocultas (modales)
const loginModal = document.getElementById('loginModal');
const cartModal = document.getElementById('cartModal');

// Atrapamos las "X" para cerrar
const closeLogin = document.getElementById('closeLogin');
const closeCart = document.getElementById('closeCart');

// Funciones para abrir y cerrar
const openModal = (modal) => {
    modal.style.display = 'flex';
    // Un respiro de 10ms para que la transición de opacidad del CSS haga su magia
    setTimeout(() => modal.classList.add('show'), 10);
};

const closeModal = (modal) => {
    modal.classList.remove('show');
    setTimeout(() => modal.style.display = 'none', 300);
};

// Al hacer clic en los íconos, abrimos las ventanas
loginBtn.addEventListener('click', () => openModal(loginModal));
cartBtn.addEventListener('click', () => openModal(cartModal));

// Al hacer clic en la X, cerramos
closeLogin.addEventListener('click', () => closeModal(loginModal));
closeCart.addEventListener('click', () => closeModal(cartModal));

// Si el usuario hace clic afuera de la caja blanca, también se cierra
window.addEventListener('click', (e) => {
    if (e.target === loginModal) closeModal(loginModal);
    if (e.target === cartModal) closeModal(cartModal);
});

// Lógica real del carrito
let cartItems = []; // Aquí guardaremos los productos
const cartItemsContainer = document.querySelector('.cart-items-container');
const cartTotalElement = document.querySelector('.cart-total span');
const cartCountElement = document.getElementById('cart-count');
const addToCartButtons = document.querySelectorAll('.btn-cart.add-to-cart');

addToCartButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        // Subimos en la estructura HTML para capturar la info de la tarjeta que tocaste
        const productCard = e.target.closest('.product-card');
        const productName = productCard.querySelector('.product-name').textContent;
        const priceText = productCard.querySelector('.product-price').textContent;
        
        // Limpiamos el texto "$4.500 CLP" para quedarnos solo con el número 4500
        const productPrice = parseInt(priceText.replace(/[^0-9]/g, ''));

        // Revisamos si el producto ya está en el carrito para sumar cantidad en vez de repetirlo
        const existingItem = cartItems.find(item => item.name === productName);
        if (existingItem) {
            existingItem.quantity++;
        } else {
            cartItems.push({ name: productName, price: productPrice, quantity: 1 });
        }

        // Feedback visual en el botón
        const originalText = button.textContent;
        button.textContent = '¡Agregado!';
        button.style.backgroundColor = 'var(--primary-hover)';
        setTimeout(() => {
            button.textContent = originalText;
            button.style.backgroundColor = '';
        }, 1000);

        // Actualizamos la vista del carrito
        updateCartUI();
    });
});

function updateCartUI() {
    // Vaciamos el contenedor visual antes de volver a llenarlo
    cartItemsContainer.innerHTML = '';
    
    let total = 0;
    let totalItems = 0;

    if (cartItems.length === 0) {
        cartItemsContainer.innerHTML = '<p class="empty-cart-msg">Tu carrito está vacío.</p>';
    } else {
        cartItems.forEach((item, index) => {
            total += item.price * item.quantity;
            totalItems += item.quantity;

            // Creamos el diseño de cada producto dentro de la lista
            const itemElement = document.createElement('div');
            itemElement.style.cssText = 'display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color);';
            itemElement.innerHTML = `
                <div>
                    <div style="font-weight: 700; font-size: 0.95rem; color: var(--text-main);">${item.name}</div>
                    <div style="font-size: 0.85rem; color: var(--text-light);">$${item.price.toLocaleString('es-CL')} x ${item.quantity}</div>
                </div>
                <button onclick="removeFromCart(${index})" style="background: none; border: none; color: #ef4444; cursor: pointer; font-size: 1.5rem; line-height: 1;" title="Eliminar">&times;</button>
            `;
            cartItemsContainer.appendChild(itemElement);
        });
    }

    // Actualizamos el número del ícono de arriba y el total a pagar
    cartCountElement.textContent = `[ ${totalItems} ]`;
    cartTotalElement.textContent = `$${total.toLocaleString('es-CL')} CLP`;
}

// Función para eliminar un producto haciendo clic en la X
window.removeFromCart = function(index) {
    cartItems.splice(index, 1);
    updateCartUI();
};

// Lógica real del buscador en vivo
const searchInput = document.getElementById('search-input');
const productCards = document.querySelectorAll('.product-card');

// Oculta/Muestra la barra al tocar la lupa
// (Nota: searchBtn ya lo habíamos declarado al principio del archivo)
searchBtn.addEventListener('click', () => {
    if (searchInput.style.display === 'none') {
        searchInput.style.display = 'inline-block';
        searchInput.focus(); // Pone el cursor listo para escribir
    } else {
        searchInput.style.display = 'none';
        searchInput.value = ''; // Limpia el texto si decides cerrarlo
        // Restaura todos los productos a la vista
        productCards.forEach(card => card.style.display = '');
    }
});

// Filtra las tarjetas mientras tecleas
searchInput.addEventListener('input', (e) => {
    const textoBuscado = e.target.value.toLowerCase();
    
    productCards.forEach(card => {
        // Lee el nombre del producto en cada tarjeta
        const nombreProducto = card.querySelector('.product-name').textContent.toLowerCase();
        
        // Si el nombre coincide con lo escrito, se muestra. Si no, se oculta.
        if (nombreProducto.includes(textoBuscado)) {
            card.style.display = ''; // Recupera su display original del CSS
        } else {
            card.style.display = 'none'; // Lo esconde
        }
    });
});