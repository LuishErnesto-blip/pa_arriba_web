// =============================================================================
// script.js - Lógica Principal de la Landing Page Pa'arriba
// Este archivo contiene todas las funciones JavaScript para la interactividad
// de la landing page, incluyendo la bombilla, acordeones, tienda, footer,
// y el comportamiento del header sticky.
// =============================================================================

// --- 1. Variables Globales (Declaradas aquí, inicializadas en DOMContentLoaded) ---
let accordionContainer;

// Variables para la Tienda
let categoryGrid;
let productListingAccordion;
let productsGrid;
let productListingTitle;
let backToCategoriesBtn;
let productDetailModal;
let closeModalBtn;
let modalProductImage;
let modalProductName;
let modalProductDescription;
let modalProductPrice;
let buyNowBtn;
let buyNowMessage;
let currentProduct = null; // Variable para almacenar el producto actual en el modal

// Variables para el Header Sticky
let stickyHeaderContent;
let stickyHeaderWrapper;
let heroSection;

// Variables para el Footer
let footerSection;
let footerHeader; // El header del acordeón del footer

// --- 2. Datos de la Tienda (Array de Productos de Ejemplo) ---
const products = [
    // 🧰 Herramientas Digitales
    { id: 'h1', name: 'Kit SEO para Negocios Locales', category: 'herramientas', description: 'Haz que tu negocio aparezca en Google y en búsquedas locales sin ser experto en SEO. Este kit incluye auditoría, palabras clave estratégicas y seguimiento práctico.', price: '49.99', image: 'https://placehold.co/150x150/E0E0E0/333333?text=SEO+Kit', impact: 'Aumenta tu visibilidad digital', targetUser: 'Emprendedores sin equipo de marketing', technicalLevel: 'Básico', timeToImplement: '1 hora' },
    { id: 'h2', name: 'Apps y Webs para Proyectos Pequeños', category: 'herramientas', description: 'Soluciones digitales personalizadas desde $9.99 para organizar, comunicar y ejecutar tareas en pequeños negocios o emprendimientos. Precio según funcionalidad.', price: '9.99', image: 'https://placehold.co/150x150/E0E0E0/333333?text=Apps+Proyectos', impact: 'Digitaliza tu operación sin complicaciones', targetUser: 'Emprendedores multitarea', technicalLevel: 'Intermedio', timeToImplement: 'Dependiendo del requerimiento' },
    { id: 'h3', name: 'App de Email Marketing para Emprendedores', category: 'herramientas', description: 'Automatiza tus campañas de correo, conecta con tus clientes y vende sin complicarte. Especialmente diseñada para emprendedores con tiempo limitado.', price: '29.99', image: 'https://placehold.co/150x150/E0E0E0/333333?text=Email+Mkt+App', impact: 'Genera clientes recurrentes con correos efectivos', targetUser: 'Negocios en crecimiento que venden online', technicalLevel: 'Básico', timeToImplement: '1 hora' },

    // 📚 Cursos y Capacitaciones
    { id: 'c1', name: 'Curso a Domicilio de Marketing Digital (20h)', category: 'cursos', description: 'Aprende a vender en redes, buscadores y por contenido desde cero. Este curso presencial está diseñado para emprendedores autodidactas que quieren dominar el marketing sin complicarse.', price: '200.00', image: 'https://placehold.co/150x150/E0E0E0/333333?text=Curso+Mkt+Domicilio', impact: 'Activa tus ventas online desde casa', targetUser: 'Emprendedores sin formación técnica', technicalLevel: 'Básico a Intermedio', timeToImplement: '20 horas presenciales' },
    { id: 'c2', name: 'Certificación en Control de Costos para Emprendedores', category: 'cursos', description: 'Aprende a calcular correctamente el precio de venta de tus productos y servicios. Este curso te da la claridad financiera que tu negocio necesita para crecer con rentabilidad.', price: '29.99', image: 'https://placehold.co/150x150/E0E0E0/333333?text=Control+de+Costos', impact: 'Optimiza tu rentabilidad desde el precio', targetUser: 'Negocios sin claridad financiera', technicalLevel: 'Básico', timeToImplement: '1 día' },
    { id: 'c3', name: 'Crea tu Web sin Programar y Vende Online (15h)', category: 'cursos', description: 'Diseña tu sitio web y activa tu canal de ventas online sin saber código. Te guiamos paso a paso para que lances tu plataforma digital en sólo 15 horas.', price: '150.00', image: 'https://placehold.co/150x150/E0E0E0/333333?text=Bootcamp+Web', impact: 'Genera presencia digital sin depender de técnicos', targetUser: 'Negocios que aún no tienen página web', technicalLevel: 'Básico', timeToImplement: '15 horas intensivas' },

    // 🧑‍💼 Servicios de Consultoría
    { id: 's1', name: 'Consultoría Estratégica Personalizada (1h)', category: 'consultoria', description: 'En esta sesión 1:1 descubrimos oportunidades, aclaramos bloqueos y trazamos acciones rentables para tu negocio. Ideal para emprendedores en fase de reinvención.', price: '9.50', image: 'https://placehold.co/150x150/E0E0E0/333333?text=Consultoria+1h', impact: 'Define tu dirección con claridad', targetUser: 'Emprendedores indecisos o en transición', technicalLevel: 'No técnico', timeToImplement: '1 hora' },
    { id: 's2', name: 'Auditoría SEO con Recomendaciones Prácticas', category: 'consultoria', description: 'Revisamos tu sitio y te entregamos un plan para posicionarte mejor en buscadores. Te decimos qué mejorar y cómo hacerlo, sin tecnicismos.', price: '36.00', image: 'https://placehold.co/150x150/E0E0E0/333333?text=Auditoría+SEO', impact: 'Atrae más clientes vía Google', targetUser: 'Negocios con página web activa', technicalLevel: 'Intermedio', timeToImplement: '3 horas estimadas' },
    { id: 's3', name: 'Mentoría Semanal de Marketing Digital (10h)', category: 'consultoria', description: 'Durante la semana, te guiamos en campañas reales, ajustes de estrategia, y generación de resultados concretos. Trabajo intensivo para negocios que quieren crecer cada semana.', price: '60.00', image: 'https://placehold.co/150x150/E0E0E0/333333?text=Mentoría+Semanal', impact: 'Evoluciona tu marketing semana a semana', targetUser: 'Negocios que necesitan acompañamiento activo', technicalLevel: 'Intermedio', timeToImplement: '10 horas semanales' },

    // 📦 Plantillas y Recursos
    { id: 'p1', name: 'Plantillas Profesionales para Redes Sociales', category: 'plantillas', description: 'Diseños modernos y editables listos para tus publicaciones en Instagram, Facebook y TikTok. Ideal para emprendedores que quieren ahorrar tiempo sin perder calidad.', price: '4.99', image: 'https://placehold.co/150x150/E0E0E0/333333?text=Plantillas+RRSS', impact: 'Publica contenido profesional sin pagar diseñador', targetUser: 'Negocios que gestionan sus propias redes', technicalLevel: 'Básico', timeToImplement: 'Menos de 1 hora' },
    { id: 'p2', name: 'Guía Editable para tu Plan de Negocios', category: 'plantillas', description: 'Completa esta guía con tus datos y define tu idea, tus costos, tus proyecciones y tu modelo. Ideal para negocios nuevos o en rediseño.', price: '9.99', image: 'https://placehold.co/150x150/E0E0E0/333333?text=Guía+Negocios', impact: 'Estructura tu idea para convertirla en empresa', targetUser: 'Emprendedores en etapa inicial', technicalLevel: 'Básico', timeToImplement: '2 horas' },
    { id: 'p3', name: 'Kit Gráfico para Emprendedores', category: 'plantillas', description: 'Recursos visuales editables que incluyen iconos, banners, fondos, y mockups para redes sociales, presentaciones y páginas web. Profesionaliza tu imagen sin pagar diseño gráfico.', price: '4.99', image: 'https://placehold.co/150x150/E0E0E0/333333?text=Kit+Gráfico', impact: 'Haz que tu marca luzca profesional desde el día uno', targetUser: 'Negocios que necesitan mejorar su imagen visual', technicalLevel: 'Básico', timeToImplement: 'Menos de 1 hora' }
];

// --- 3. Funciones Principales y de Utilidad ---


/**
 * Función para colapsar todas las tarjetas de acordeón.
 * NO limpia sessionStorage aquí, eso se hace en toggleAccordionCard cuando una tarjeta se colapsa.
 */
const collapseAllAccordions = () => {
    console.log("collapseAllAccordions called.");
    document.querySelectorAll('.accordion-card.expanded').forEach(card => {
        card.classList.remove('expanded');
        const content = card.querySelector('.accordion-content');
        if (content) {
            content.style.maxHeight = '0';
        }
        // Asegura que el icono vuelva a '+'
        const icon = card.querySelector('.accordion-icon');
        if (icon) icon.textContent = '+';
        // Oculta el wrapper interno si es necesario
        const currentContentInnerWrapper = content.querySelector('div');
        if (currentContentInnerWrapper) {
            currentContentInnerWrapper.style.display = 'none';
        }
    });
    console.log("All accordions visually collapsed.");
};



/**
 * Abre WhatsApp con un mensaje predefinido para prototipos.
 * @param {string} prototypeName - El nombre del prototipo que interesa al usuario.
 */
function openWhatsAppForPrototype(prototypeName) {
    const phoneNumber = '593997277796';
    const message = `¡Hola! Me interesa el prototipo "${prototypeName}". ¿Podrías darme más información?`;
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
}

/**
 * Expande o contrae una tarjeta de acordeón. Cierra otras tarjetas abiertas.
 * @param {Event} event - El evento de clic que disparó la función.
 */
function toggleAccordionCard(event) {
    const header = event.currentTarget;
    const card = header.closest('.accordion-card');
    const content = card.querySelector('.accordion-content');
    const icon = header.querySelector('.accordion-icon');
    const cardId = card.id; // Obtiene el ID de la tarjeta

    console.log(`toggleAccordionCard called for: ${cardId}`);

    // Colapsar todas las otras tarjetas expandidas antes de expandir esta
    // Excepto si es la tarjeta que ya está expandida y se va a colapsar
    document.querySelectorAll('.accordion-card.expanded').forEach(openCard => {
        if (openCard !== card && !openCard.classList.contains('footer-card')) {
            console.log(`Collapsing other card: ${openCard.id}`);
            openCard.classList.remove('expanded');
            const openCardContent = openCard.querySelector('.accordion-content');
            if (openCardContent) openCardContent.style.maxHeight = '0';
            const openCardIcon = openCard.querySelector('.accordion-icon');
            if (openCardIcon) openCardIcon.textContent = '+'; // Icono a '+'
            const openCardContentInnerWrapper = openCard.querySelector('.accordion-content > div');
            if (openCardContentInnerWrapper) openCardContentInnerWrapper.style.display = 'none';
            openCard.querySelectorAll('.prototipo-video').forEach(video => {
                video.pause();
                video.currentTime = 0;
            });
            if (openCard.id === 'tienda-card') {
                if (categoryGrid) categoryGrid.classList.remove('hidden');
                if (productListingAccordion) productListingAccordion.classList.add('hidden');
                toggleProductListingAccordion(false);
            }
            // Limpia sessionStorage solo si la tarjeta que se colapsa es la que estaba guardada
            if (sessionStorage.getItem('expandedAccordionId') === openCard.id) {
                console.log(`Removing ${openCard.id} from sessionStorage.`);
                sessionStorage.removeItem('expandedAccordionId');
            }
        }
    });

    card.classList.toggle('expanded');
    const currentContentInnerWrapper = content.querySelector('div');

    if (card.classList.contains('expanded')) {
        console.log(`Expanding card: ${cardId}`);
        if (currentContentInnerWrapper) {
            currentContentInnerWrapper.style.display = 'block';
        }
        if (content && currentContentInnerWrapper) content.style.maxHeight = currentContentInnerWrapper.scrollHeight + 'px';
        if (icon) icon.textContent = '-'; // Icono a '-'
        card.querySelectorAll('.prototipo-video').forEach(video => {
            video.play().catch(e => console.error("Error al reproducir video de prototipo:", e));
        });
        sessionStorage.setItem('expandedAccordionId', cardId); // Guarda el ID de la tarjeta expandida
        console.log(`Stored ${cardId} in sessionStorage.`);

        // --- INICIO DE LA MODIFICACIÓN CRÍTICA: Añadir hash a la URL ---
        history.pushState(null, '', `#${cardId}`);
        console.log(`URL hash set to #${cardId}.`);
        // --- FIN DE LA LA MODIFICACIÓN CRÍTICA ---

    } else {
        console.log(`Collapsing card: ${cardId}`);
        if (content) content.style.maxHeight = '0';
        if (icon) icon.textContent = '+'; // Icono a '+'
        if (currentContentInnerWrapper) {
            currentContentInnerWrapper.style.display = 'none';
        }
        card.querySelectorAll('.prototipo-video').forEach(video => {
            video.pause();
            video.currentTime = 0;
        });
        if (card.id === 'tienda-card') {
            if (categoryGrid) categoryGrid.classList.remove('hidden');
            if (productListingAccordion) productListingAccordion.classList.add('hidden');
            toggleProductListingAccordion(false);
        }
        sessionStorage.removeItem('expandedAccordionId'); // Elimina el ID si la tarjeta actual se colapsa
        console.log(`Removed ${cardId} from sessionStorage.`);

        // --- INICIO DE LA MODIFICACIÓN CRÍTICA: Eliminar hash de la URL ---
        history.pushState(null, '', window.location.pathname + window.location.search);
        console.log("URL hash removed.");
        // --- FIN DE LA LA MODIFICACIÓN CRÍTICA ---
    }
}

/**
 * Maneja la expansión/colapso del acordeón de productos destacados dentro de la tienda.
 * @param {boolean} expand - Si es `true`, expande el acordeón; si es `false`, lo colapsa.
 */
function toggleProductListingAccordion(expand = false) {
    if (!productListingAccordion) return;

    const productListingHeader = productListingAccordion.querySelector('.product-listing-header');
    const productListingContent = productListingAccordion.querySelector('.product-listing-content');
    const productListingIcon = productListingHeader ? productListingHeader.querySelector('.accordion-icon') : null;

    if (expand) {
        productListingAccordion.classList.add('expanded');
        productListingAccordion.classList.remove('hidden');
        setTimeout(() => {
            if (productListingContent) productListingContent.style.maxHeight = productListingContent.scrollHeight + 'px';
        }, 10);
        if (productListingIcon) productListingIcon.textContent = '-';
    } else {
        productListingAccordion.classList.remove('expanded');
        if (productListingContent) productListingContent.style.maxHeight = '0';
        if (productListingIcon) productListingIcon.textContent = '+';
        setTimeout(() => {
            productListingAccordion.classList.add('hidden');
        }, 300);
    }
}


/**
 * Maneja el clic en el botón "Comprar Ahora" del modal de productos.
 * Redirige al usuario a WhatsApp con un mensaje predefinido.
 */
function handleBuyNow() {
    if (!currentProduct || !buyNowMessage || !buyNowBtn) {
        console.error("Elementos necesarios para handleBuyNow no encontrados.");
        return;
    }

    buyNowMessage.textContent = 'Redirigiendo a WhatsApp...';
    buyNowMessage.classList.remove('hidden');

    buyNowBtn.disabled = true;
    buyNowBtn.classList.add('opacity-50', 'cursor-not-allowed');

    const phoneNumber = '593997277796';
    const message = `¡Hola! Me interesa el producto "${currentProduct.name}" con un precio de $${currentProduct.price}. ¿Podrías darme más información?`;
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;

    setTimeout(() => {
        window.open(whatsappUrl, '_blank');
        closeProductModal();
        buyNowBtn.disabled = false;
        buyNowBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }, 100);
}

/**
 * Abre el modal de detalles del producto con la información del producto dado.
 * @param {string} productId - El ID del producto a mostrar.
 */
function openProductModal(productId) {
    currentProduct = products.find(p => p.id === productId);
    if (currentProduct) {
        if (modalProductImage) modalProductImage.src = currentProduct.image;
        if (modalProductImage) modalProductImage.alt = currentProduct.name;
        if (modalProductName) modalProductName.textContent = currentProduct.name;
        if (modalProductDescription) modalProductDescription.textContent = currentProduct.description;
        if (modalProductPrice) modalProductPrice.textContent = `$${currentProduct.price}`;

        if (buyNowMessage) {
            buyNowMessage.classList.add('hidden');
            buyNowMessage.textContent = '';
        }

        if (productDetailModal) {
            productDetailModal.classList.remove('hidden');
            setTimeout(() => {
                const modalContentDiv = productDetailModal.querySelector('div');
                if (modalContentDiv) {
                    modalContentDiv.classList.remove('scale-95', 'opacity-0');
                    modalContentDiv.classList.add('scale-100', 'opacity-100');
                }
            }, 10);
        }
    }
}

/**
 * Cierra el modal de detalles del producto.
 */
function closeProductModal() {
    if (productDetailModal) {
        const modalContentDiv = productDetailModal.querySelector('div');
        if (modalContentDiv) {
            modalContentDiv.classList.remove('scale-100', 'opacity-100');
            modalContentDiv.classList.add('scale-95', 'opacity-0');
        }
        setTimeout(() => {
            productDetailModal.classList.add('hidden');
            currentProduct = null;
        }, 300);
    }
}

/**
 * Muestra los productos en el grid de la tienda, filtrando por categoría si se especifica.
 * @param {string|null} category - La categoría a filtrar, o `null` para mostrar todas las categorías.
 */
function displayProducts(category = null) {
    if (!productsGrid || !categoryGrid || !productListingAccordion || !productListingTitle) {
        console.error("Elementos de la tienda no encontrados en displayProducts. Asegúrate de que los IDs son correctos.");
        return;
    }

    productsGrid.innerHTML = '';
    let filteredProducts = products;
    let titleText = "Productos Destacados";

    if (category) {
        filteredProducts = products.filter(product => product.category === category);
        titleText = `Productos de ${category.charAt(0).toUpperCase() + category.slice(1)}`;
        categoryGrid.classList.add('hidden');
        productListingAccordion.classList.remove('hidden');
        toggleProductListingAccordion(true);
    } else {
        categoryGrid.classList.remove('hidden');
        productListingAccordion.classList.add('hidden');
        toggleProductListingAccordion(false);
    }

    productListingTitle.textContent = titleText;

    if (filteredProducts.length > 0) {
        filteredProducts.forEach(product => {
            const productCard = `
                <div class="product-card bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition-shadow duration-300 transform hover:scale-105 cursor-pointer flex flex-col items-center text-center border border-gray-200">
                    <div>
                        <img src="${product.image}" alt="${product.name}" class="w-32 h-32 object-cover rounded-lg mx-auto mb-4">
                        <h4 class="text-xl font-semibold text-gray-800 mb-2">${product.name}</h4>
                        <p class="text-gray-600 text-sm mb-3">${product.description}</p>
                        <div class="text-sm text-gray-700 mb-3 space-y-1 text-left">
                            <p><strong>Impacto:</strong> ${product.impact || '—'}</p>
                            <p><strong>Para:</strong> ${product.targetUser || '—'}</p>
                            <p><strong>Nivel técnico:</strong> ${product.technicalLevel || '—'}</p>
                            <p><strong>Implementación:</strong> ${product.timeToImplement || '—'}</p>
                        </div>
                        <span class="text-pa-arriba-orange-force font-bold text-lg mb-4 block">$${product.price}</span>
                    </div>
                    <button class="cta-button-small text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors duration-300 w-full" style="background-color: #ff5c00;" data-product-id="${product.id}">
                        Ver Detalles
                    </button>
                </div>
            `;
            productsGrid.innerHTML += productCard;
        });

        productsGrid.querySelectorAll('.cta-button-small[data-product-id]').forEach(button => {
            button.addEventListener('click', (event) => {
                const productId = event.target.dataset.productId;
                openProductModal(productId);
            });
        });
    } else {
        productsGrid.innerHTML = '<p class="text-gray-600">No hay productos disponibles en esta categoría.</p>';
    }
}

/**
 * Alterna la expansión/colapso del footer.
 * Expande el footer si está colapsado y viceversa.
 */
function toggleFooterAccordion() {
    console.log("toggleFooterAccordion called.");
    if (!footerSection) {
        console.error("Footer section no encontrado en toggleFooterAccordion. No se puede alternar.");
        return;
    }

    const content = footerSection.querySelector('.footer-accordion-content');
    const icon = footerSection.querySelector('.accordion-icon');

    if (!content || !icon) {
        console.error("Contenido o icono del footer-accordion no encontrado dentro de footerSection.");
        console.log("footerSection:", footerSection);
        console.log("content:", content);
        console.log("icon:", icon);
        return;
    }

    footerSection.classList.toggle('expanded');
    console.log("footerSection classes after toggle:", footerSection.classList);

    if (footerSection.classList.contains('expanded')) {
        content.style.maxHeight = content.scrollHeight + 'px';
        icon.textContent = '-';
    } else {
        content.style.maxHeight = '0';
        icon.textContent = '+';
    }
}

// --- 4. Funciones de Configuración (Setup Functions) ---

/**
 * Configura los event listeners para las tarjetas de acordeón principales (Filosofía, Prototipos, Testimonios).
 */
function setupAccordionCards() {
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    accordionHeaders.forEach(header => {
        if (!header.classList.contains('footer-accordion-header')) {
            header.addEventListener('click', toggleAccordionCard);
        }
    });

    const footerCollapseButtons = document.querySelectorAll('.accordion-footer-collapse-btn');
    footerCollapseButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.stopPropagation(); // Evita que el clic se propague al encabezado del acordeón
            const card = event.target.closest('.accordion-card');
            if (card) {
                // Simula un clic en el encabezado para activar toggleAccordionCard
                const headerToClick = card.querySelector('.accordion-header');
                if (headerToClick) {
                    headerToClick.click();
                }
            }
        });
    });
}

/**
 * Configura el event listener para el botón principal de WhatsApp (si existe).
 */
function setupWhatsAppButton() {
    const whatsappMainButton = document.getElementById('whatsappMainButton');
    if (whatsappMainButton) {
        whatsappMainButton.addEventListener('click', () => {
            openWhatsAppForPrototype('Consulta General');
        });
    }
}

/**
 * Configura toda la lógica relacionada con la tienda:
 * Event listeners para categorías, botones de productos, modal, etc.
 */
function setupStoreLogic() {
    if (!categoryGrid || !productListingAccordion || !productsGrid || !productListingTitle || !backToCategoriesBtn || !productDetailModal || !closeModalBtn || !buyNowBtn) {
        console.error("No se pudieron encontrar todos los elementos de la tienda en setupStoreLogic. Asegúrate de que los IDs son correctos.");
        return;
    }

    categoryGrid.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', () => {
            const category = card.dataset.category;
            displayProducts(category);
        });
    });

    backToCategoriesBtn.addEventListener('click', () => {
        displayProducts(null);
    });

    productListingAccordion.querySelector('.product-listing-header').addEventListener('click', () => {
        toggleProductListingAccordion(productListingAccordion.classList.contains('expanded') ? false : true);
    });

    productListingAccordion.querySelector('.product-listing-content .accordion-footer-collapse-btn').addEventListener('click', () => {
        toggleProductListingAccordion(false);
    });

    closeModalBtn.addEventListener('click', closeProductModal);
    productDetailModal.addEventListener('click', (event) => {
        if (event.target === productDetailModal) {
            closeProductModal();
        }
    });

    buyNowBtn.addEventListener('click', handleBuyNow);

    displayProducts(null); // Mostrar productos destacados al cargar la página inicialmente
}

/**
 * Configura el comportamiento del header sticky al hacer scroll.
 */
function setupStickyHeader() {
    if (!stickyHeaderContent || !stickyHeaderWrapper || !heroSection) {
        console.error("Elementos del header sticky no encontrados.");
        return;
    }

    window.addEventListener('scroll', function() {
        const stickyHeight = stickyHeaderContent.offsetHeight;
        const activationPoint = heroSection.offsetHeight - stickyHeight;

        if (window.scrollY > activationPoint) {
            stickyHeaderContent.classList.add('is-sticky');
            stickyHeaderWrapper.style.height = stickyHeight + 'px';
        } else {
            stickyHeaderContent.classList.remove('is-sticky');
            stickyHeaderWrapper.style.height = 'auto';
        }
    });
}

/**
 * Configura el footer colapsable.
 */
function setupFooterAccordion() {
    console.log("setupFooterAccordion called.");
    if (!footerHeader) {
        console.error("Header del footer no encontrado en setupFooterAccordion. No se puede configurar el listener.");
        return;
    }
    footerHeader.addEventListener('click', toggleFooterAccordion);
    console.log("Listener añadido al footerHeader.");
    toggleFooterAccordion(); // Expandir el footer por defecto al cargar la página
    console.log("toggleFooterAccordion llamado para expandir por defecto.");
}


// --- 5. Ejecución al Cargar el DOM ---

// Asegura que el DOM esté completamente cargado antes de ejecutar los scripts
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOMContentLoaded fired. Initializing global DOM element references...");

    // Inicializar referencias a elementos del DOM
    accordionContainer = document.getElementById('accordion-container');
    console.log("accordionContainer:", accordionContainer); // Log para verificar
    if (!accordionContainer) console.error("ERROR: #accordion-container no encontrado.");

    categoryGrid = document.getElementById('category-grid');
    console.log("categoryGrid:", categoryGrid); // Log para verificar
    if (!categoryGrid) console.error("ERROR: #category-grid (tienda) no encontrado.");

    productListingAccordion = document.getElementById('product-listing-accordion');
    console.log("productListingAccordion:", productListingAccordion); // Log para verificar
    if (!productListingAccordion) console.error("ERROR: #product-listing-accordion (tienda) no encontrado.");

    productsGrid = document.getElementById('products-grid');
    console.log("productsGrid:", productsGrid); // Log para verificar
    if (!productsGrid) console.error("ERROR: #products-grid (tienda) no encontrado.");

    productListingTitle = document.getElementById('product-listing-title');
    console.log("productListingTitle:", productListingTitle); // Log para verificar
    if (!productListingTitle) console.error("ERROR: #product-listing-title (tienda) no encontrado.");

    backToCategoriesBtn = document.getElementById('back-to-categories-btn');
    console.log("backToCategoriesBtn:", backToCategoriesBtn); // Log para verificar
    if (!backToCategoriesBtn) console.error("ERROR: #back-to-categories-btn (tienda) no encontrado.");

    productDetailModal = document.getElementById('product-detail-modal');
    console.log("productDetailModal:", productDetailModal); // Log para verificar
    if (!productDetailModal) console.error("ERROR: #product-detail-modal (tienda) no encontrado.");

    closeModalBtn = document.getElementById('close-modal-btn');
    console.log("closeModalBtn:", closeModalBtn); // Log para verificar
    if (!closeModalBtn) console.error("ERROR: #close-modal-btn (modal tienda) no encontrado.");

    modalProductImage = document.getElementById('modal-product-image');
    console.log("modalProductImage:", modalProductImage); // Log para verificar
    if (!modalProductImage) console.error("ERROR: #modal-product-image (modal tienda) no encontrado.");

    modalProductName = document.getElementById('modal-product-name');
    console.log("modalProductName:", modalProductName); // Log para verificar
    if (!modalProductName) console.error("ERROR: #modal-product-name (modal tienda) no encontrado.");

    modalProductDescription = document.getElementById('modal-product-description');
    console.log("modalProductDescription:", modalProductDescription); // Log para verificar
    if (!modalProductDescription) console.error("ERROR: #modal-product-description (modal tienda) no encontrado.");

    modalProductPrice = document.getElementById('modal-product-price');
    console.log("modalProductPrice:", modalProductPrice); // Log para verificar
    if (!modalProductPrice) console.error("ERROR: #modal-product-price (modal tienda) no encontrado.");

    buyNowBtn = document.getElementById('buy-now-btn');
    console.log("buyNowBtn:", buyNowBtn); // Log para verificar
    if (!buyNowBtn) console.error("ERROR: #buy-now-btn (modal tienda) no encontrado.");

    buyNowMessage = document.getElementById('buy-now-message');
    console.log("buyNowMessage:", buyNowMessage); // Log para verificar
    if (!buyNowMessage) console.error("ERROR: #buy-now-message (modal tienda) no encontrado.");

    stickyHeaderContent = document.querySelector('.sticky-header-content');
    console.log("stickyHeaderContent:", stickyHeaderContent); // Log para verificar
    if (!stickyHeaderContent) console.error("ERROR: .sticky-header-content no encontrado.");

    stickyHeaderWrapper = document.querySelector('.sticky-header-wrapper');
    console.log("stickyHeaderWrapper:", stickyHeaderWrapper); // Log para verificar
    if (!stickyHeaderWrapper) console.error("ERROR: .sticky-header-wrapper no encontrado.");

    heroSection = document.querySelector('.hero-section');
    console.log("heroSection:", heroSection); // Log para verificar
    if (!heroSection) console.error("ERROR: .hero-section no encontrado.");

    footerSection = document.querySelector('.footer-section');
    console.log("footerSection:", footerSection); // Log para verificar
    if (!footerSection) console.error("ERROR: .footer-section no encontrado.");

    // IMPORTANTE: footerHeader se busca DENTRO de footerSection, así que footerSection debe existir primero
    if (footerSection) {
        footerHeader = footerSection.querySelector('.footer-accordion-header');
        console.log("footerHeader (después de buscar dentro de footerSection):", footerHeader); // Log para verificar
        if (!footerHeader) console.error("ERROR: .footer-accordion-header NO encontrado DENTRO de .footer-section.");
    } else {
        console.error("ERROR CRÍTICO: footerSection es null, no se puede buscar footerHeader.");
    }


    // Llamar a las funciones de configuración
    console.log("Calling setup functions...");
    setupAccordionCards();
    setupStoreLogic();
    setupStickyHeader();
    setupWhatsAppButton();
    setupFooterAccordion(); // Esta función ahora tiene la comprobación interna
    console.log("Setup functions called.");

    // NUEVA LÓGICA: Restaurar el estado del acordeón al cargar la página
    const storedAccordionId = sessionStorage.getItem('expandedAccordionId');
    const hash = window.location.hash;

    console.log("DOMContentLoaded: Checking for hash or storedAccordionId.");
    console.log("Current hash:", hash);
    console.log("Stored Accordion ID:", storedAccordionId);

    // Prioriza el hash si existe y es válido
    if (hash) {
        console.log("Hash detected:", hash);
        const targetCard = document.querySelector(hash);
        if (targetCard && targetCard.classList.contains('accordion-card')) {
            console.log("Target card found by hash:", targetCard.id);
            // No colapsamos todas las tarjetas aquí, la lógica de expansión lo hará
            // y colapsará las demás si es necesario.
            
            // Simular un clic en el encabezado de la tarjeta objetivo para activar toggleAccordionCard
            const targetHeader = targetCard.querySelector('.accordion-header');
            if (targetHeader) {
                targetHeader.click(); // Esto expandirá la tarjeta y actualizará el icono
                console.log("Simulated click on target card header via hash.");
            } else {
                console.warn("Target card header not found for hash:", hash);
            }
        } else {
            console.warn("Target card not found or not an accordion-card for hash:", hash);
            // Si el hash no lleva a una tarjeta de acordeón, limpiar el hash para una URL limpia
            history.replaceState(null, document.title, window.location.pathname + window.location.search);
        }
    } else if (storedAccordionId) { // Si no hay hash, usa el ID guardado
        console.log("Stored ID detected:", storedAccordionId);
        const targetCard = document.getElementById(storedAccordionId);
        if (targetCard && targetCard.classList.contains('accordion-card')) {
            console.log("Target card found by stored ID:", targetCard.id);
            
            // Simular un clic en el encabezado de la tarjeta objetivo para activar toggleAccordionCard
            const targetHeader = targetCard.querySelector('.accordion-header');
            if (targetHeader) {
                targetHeader.click(); // Esto expandirá la tarjeta y actualizará el icono
                console.log("Simulated click on target card header via stored ID.");
            } else {
                console.warn("Target card header not found for stored ID:", storedAccordionId);
            }
        } else {
            console.warn("Target card not found or not an accordion-card for stored ID:", storedAccordionId);
            sessionStorage.removeItem('expandedAccordionId'); // Limpiar ID si no es válido
        }
    } else {
        console.log("No hash or stored ID found. Page will load in default state (bombilla apagada).");
    }
});





