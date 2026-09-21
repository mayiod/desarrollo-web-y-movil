
const loginBtn = document.getElementById('login-btn');
const cartBtn = document.getElementById('cart-btn');
const searchBtn = document.getElementById('search-btn');

const loginModal = document.getElementById('loginModal');
const cartModal = document.getElementById('cartModal');

const closeLogin = document.getElementById('closeLogin');
const closeCart = document.getElementById('closeCart');

const openModal = (modal) => {
    modal.style.display = 'flex';
    setTimeout(() => modal.classList.add('show'), 10);
};

const closeModal = (modal) => {
    modal.classList.remove('show');
    setTimeout(() => modal.style.display = 'none', 300);
};

loginBtn.addEventListener('click', () => openModal(loginModal));
cartBtn.addEventListener('click', () => openModal(cartModal));
searchBtn.addEventListener('click', () => {
    const searchInput = document.getElementById('search-input');
    if (searchInput.style.display === 'none') {
        searchInput.style.display = 'block';
    } else {
        searchInput.style.display = 'none';
    }
});

closeLogin.addEventListener('click', () => closeModal(loginModal));
closeCart.addEventListener('click', () => closeModal(cartModal));
window.addEventListener('click', (e) => {
    if (e.target === loginModal) closeModal(loginModal);
    if (e.target === cartModal) closeModal(cartModal);
});

let cartItems = [];
const cartItemsContainer = document.querySelector('.cart-items-container');
const cartTotalElement = document.querySelector('.cart-total span');
const cartCountElement = document.getElementById('cart-count');
const addToCartButtons = document.querySelectorAll('.btn-cart.add-to-cart');

addToCartButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        const productCard = e.target.closest('.product-card');
        const productName = productCard.querySelector('.product-name').textContent;
        const priceText = productCard.querySelector('.product-price').textContent;
        
        const productPrice = parseInt(priceText.replace(/[^0-9]/g, ''));

        const existingItem = cartItems.find(item => item.name === productName);
        if (existingItem) {
            existingItem.quantity++;
        } else {
            cartItems.push({ name: productName, price: productPrice, quantity: 1 });
        }

        const originalText = button.textContent;
        button.textContent = '¡Agregado!';
        button.style.backgroundColor = 'var(--primary-hover)';
        setTimeout(() => {
            button.textContent = originalText;
            button.style.backgroundColor = '';
        }, 1000);

        updateCartUI();
    });
});

function updateCartUI() {
    cartItemsContainer.innerHTML = '';
    
    let total = 0;
    let totalItems = 0;

    if (cartItems.length === 0) {
        cartItemsContainer.innerHTML = '<p class="empty-cart-msg">Tu carrito está vacío.</p>';
    } else {
        cartItems.forEach((item, index) => {
            total += item.price * item.quantity;
            totalItems += item.quantity;

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

    cartCountElement.textContent = `[ ${totalItems} ]`;
    cartTotalElement.textContent = `$${total.toLocaleString('es-CL')} CLP`;
}

window.removeFromCart = function(index) {
    cartItems.splice(index, 1);
    updateCartUI();
};

const searchInput = document.getElementById('search-input');
const productCards = document.querySelectorAll('.product-card');

searchBtn.addEventListener('click', () => {
    if (searchInput.style.display === 'none') {
        searchInput.style.display = 'inline-block';
        searchInput.focus();
    } else {
        searchInput.style.display = 'none';
        searchInput.value = ''; 
        productCards.forEach(card => card.style.display = '');
    }
});

searchInput.addEventListener('input', (e) => {
    const textoBuscado = e.target.value.toLowerCase();
    
    productCards.forEach(card => {
        const nombreProducto = card.querySelector('.product-name').textContent.toLowerCase();
        if (nombreProducto.includes(textoBuscado)) {
            card.style.display = ''; 
        } else {
            card.style.display = 'none'; 
        }
    });
});