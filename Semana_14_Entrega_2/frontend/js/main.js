document.addEventListener('DOMContentLoaded', () => {
    // --- Referencias al DOM ---
    const loginBtn = document.getElementById('login-btn');
    const cartBtn = document.getElementById('cart-btn');
    const searchBtn = document.getElementById('search-btn');
    
    const searchContainer = document.getElementById('search-container'); 
    const searchInput = document.getElementById('search-input');

    const loginModal = document.getElementById('loginModal');
    const cartModal = document.getElementById('cartModal');
    const closeLogin = document.getElementById('closeLogin');
    const closeCart = document.getElementById('closeCart');

    // --- Modales ---
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

    closeLogin.addEventListener('click', () => closeModal(loginModal));
    closeCart.addEventListener('click', () => closeModal(cartModal));
    
    window.addEventListener('click', (e) => {
        if (e.target === loginModal) closeModal(loginModal);
        if (e.target === cartModal) closeModal(cartModal);
    });

    // --- Cargar mas productos ---
    let heladosLoaded = false;
    let paletasLoaded = false;

    const loadMoreHeladosBtn = document.getElementById('load-more-helados');
    if (loadMoreHeladosBtn) {
        loadMoreHeladosBtn.addEventListener('click', () => {
            heladosLoaded = true; 
            const extraHelados = document.querySelectorAll('.extra-helados');
            extraHelados.forEach(card => {
                card.style.display = 'flex'; 
            });
            loadMoreHeladosBtn.style.display = 'none';
        });
    }

    const loadMorePaletasBtn = document.getElementById('load-more-paletas');
    if (loadMorePaletasBtn) {
        loadMorePaletasBtn.addEventListener('click', () => {
            paletasLoaded = true; 
            const extraPaletas = document.querySelectorAll('.extra-paletas');
            extraPaletas.forEach(card => {
                card.style.display = 'flex'; 
            });
            loadMorePaletasBtn.style.display = 'none';
        });
    }

    // --- Buscador ---
    const productCards = document.querySelectorAll('.product-card');

    searchBtn.addEventListener('click', (e) => {
        e.preventDefault(); 

        if (searchContainer.style.display === 'block') {
            searchContainer.style.display = 'none';
            searchInput.value = ''; 
            
            productCards.forEach(card => {
                if (card.classList.contains('extra-helados') && !heladosLoaded) {
                    card.style.display = 'none'; 
                } else if (card.classList.contains('extra-paletas') && !paletasLoaded) {
                    card.style.display = 'none'; 
                } else {
                    card.style.display = 'flex'; 
                }
            }); 
        } else {
            searchContainer.style.display = 'block';
            
            if (window.innerWidth >= 992) {
                 // PC
                 searchContainer.style.position = 'absolute';
                 searchContainer.style.left = 'auto';
                 searchContainer.style.right = '100%';
                 searchContainer.style.top = '50%';
                 searchContainer.style.transform = 'translateY(-50%)';
                 searchContainer.style.marginRight = '15px';
                 searchContainer.style.marginBottom = '0';
            } else {
                 // Celular
                 searchContainer.style.position = 'absolute'; 
                 searchContainer.style.left = '0';
                 searchContainer.style.right = '0';
                 searchContainer.style.top = '100%'; 
                 searchContainer.style.transform = 'none';
                 searchContainer.style.marginRight = '0';
                 searchContainer.style.marginBottom = '15px'; 
                 searchContainer.style.maxWidth = '100%';
            }

            searchInput.focus();
        }
    });

    searchInput.addEventListener('input', (e) => {
        const textoBuscado = e.target.value.toLowerCase();
        
        productCards.forEach(card => {
            if (card.classList.contains('extra-helados') && !heladosLoaded) {
                card.style.display = 'none';
                return;
            }
            if (card.classList.contains('extra-paletas') && !paletasLoaded) {
                card.style.display = 'none';
                return;
            }

            const nameEl = card.querySelector('.product-name');
            if (nameEl) {
                const nombreProducto = nameEl.textContent.toLowerCase();
                if (nombreProducto.includes(textoBuscado)) {
                    card.style.display = 'flex'; 
                } else {
                    card.style.display = 'none'; 
                }
            }
        });
    });

    // --- Carrito ---
    let cartItems = [];
    const cartItemsContainer = document.querySelector('.cart-items-container');
    const cartTotalElement = document.querySelector('.cart-total span');
    const cartCountElement = document.getElementById('cart-count');

    document.addEventListener('click', (e) => {
        if (e.target && e.target.classList.contains('add-to-cart')) {
            const button = e.target;
            const productCard = button.closest('.product-card');
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
        }
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

        if (cartCountElement) {
            cartCountElement.textContent = `[ ${totalItems} ]`;
        }
        cartTotalElement.textContent = `$${total.toLocaleString('es-CL')} CLP`;
    }

    window.removeFromCart = function(index) {
        cartItems.splice(index, 1);
        updateCartUI();
    };
});