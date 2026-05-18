const API_BASE_URL = 'http://localhost:8000';

const defaultSettings = {
    site_name: '南竹竹制品',
    stat_product_count: '500+',
    stat_sales_amount: '3000万+',
    stat_dealer_count: '50+',
    contact_address: '福建省龙岩市长汀县工业园区',
    contact_phone: '0597-1234567',
    contact_email: 'contact@nanzhu-bamboo.com',
    contact_hours: '周一至周六 8:00-18:00'
};

let settings = { ...defaultSettings };

const defaultProducts = [
    { id: 1, name: '天然竹筷套装', category: 'kitchen', price: 29.90, description: '精选优质楠竹，手工打磨，环保健康', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=premium%20bamboo%20chopsticks%20set%20elegant%20white%20background%20product%20photography%20minimalist%20style&image_size=square_hd' },
    { id: 2, name: '竹制砧板', category: 'kitchen', price: 89.00, description: '高密度竹材，抗菌耐用，家用必备', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20cutting%20board%20kitchen%20utensil%20white%20background%20product%20photography%20clean%20minimalist&image_size=square_hd' },
    { id: 3, name: '竹制收纳盒', category: 'home', price: 45.00, description: '多功能收纳，简约设计，整洁生活', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20storage%20box%20organizer%20home%20decor%20white%20background%20product%20photography%20minimalist&image_size=square_hd' },
    { id: 4, name: '竹制茶盘', category: 'craft', price: 158.00, description: '功夫茶必备，榫卯结构，排水顺畅', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=elegant%20bamboo%20tea%20tray%20kung%20fu%20tea%20ceremony%20white%20background%20product%20photography&image_size=square_hd' },
    { id: 5, name: '竹制办公收纳', category: 'office', price: 68.00, description: '简约时尚，提升办公效率', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20desk%20organizer%20pen%20holder%20office%20supplies%20white%20background%20product%20photography&image_size=square_hd' },
    { id: 6, name: '竹制餐具套装', category: 'kitchen', price: 59.00, description: '天然环保，健康生活从餐具开始', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20bowl%20set%20with%20chopsticks%20tableware%20white%20background%20product%20photography%20elegant&image_size=square_hd' }
];

let products = [];

async function fetchSettings() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/settings`);
        if (response.ok) {
            settings = { ...defaultSettings, ...await response.json() };
        }
    } catch (error) {
        console.error('Failed to fetch settings:', error);
    }
    renderSettings();
}

function renderSettings() {
    const statProduct = document.getElementById('stat-product-count');
    const statSales = document.getElementById('stat-sales-amount');
    const statDealer = document.getElementById('stat-dealer-count');
    if (statProduct) statProduct.textContent = settings.stat_product_count;
    if (statSales) statSales.textContent = settings.stat_sales_amount;
    if (statDealer) statDealer.textContent = settings.stat_dealer_count;

    const contactAddress = document.getElementById('contact-address');
    const contactPhone = document.getElementById('contact-phone');
    const contactEmail = document.getElementById('contact-email');
    const contactHours = document.getElementById('contact-hours');
    if (contactAddress) contactAddress.textContent = settings.contact_address;
    if (contactPhone) contactPhone.textContent = settings.contact_phone;
    if (contactEmail) contactEmail.textContent = settings.contact_email;
    if (contactHours) contactHours.textContent = settings.contact_hours;

    const footerPhone = document.getElementById('footer-phone');
    const footerEmail = document.getElementById('footer-email');
    const footerAddress = document.getElementById('footer-address');
    if (footerPhone) footerPhone.textContent = `电话：${settings.contact_phone}`;
    if (footerEmail) footerEmail.textContent = `邮箱：${settings.contact_email}`;
    if (footerAddress) footerAddress.textContent = `地址：${settings.contact_address}`;
}

async function fetchProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/products`);
        if (response.ok) products = await response.json();
        else products = [...defaultProducts];
    } catch (error) {
        console.error('Failed to fetch products:', error);
        products = [...defaultProducts];
    }
    renderProducts();
}

function renderProducts() {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;
    grid.innerHTML = products.map(product => `
        <div class="product-card" data-category="${product.category}">
            <div class="product-image">
                <img src="${product.image}" alt="${product.name}" onerror="this.src='https://via.placeholder.com/400x300/228B22/ffffff?text=${encodeURIComponent(product.name)}'">
            </div>
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description}</p>
                <div class="product-price">¥${product.price.toFixed(2)}</div>
                <button class="btn btn-outline">查看详情</button>
            </div>
        </div>
    `).join('');
    initProductFilters();
    initScrollAnimations();
}

function initProductFilters() {
    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const filter = this.getAttribute('data-filter');
            document.querySelectorAll('.product-card').forEach(card => {
                card.style.display = (filter === 'all' || card.getAttribute('data-category') === filter) ? 'block' : 'none';
            });
        });
    });
}

async function submitContactForm(e) {
    e.preventDefault();
    const data = {
        name: document.getElementById('contactName').value,
        email: document.getElementById('contactEmail').value,
        phone: document.getElementById('contactPhone').value,
        content: document.getElementById('contactContent').value,
        status: 'pending'
    };
    try {
        const response = await fetch(`${API_BASE_URL}/api/messages`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('感谢您的留言！我们会尽快与您联系。');
            e.target.reset();
        }
    } catch (error) {
        console.error('Failed to submit message:', error);
        alert('留言已提交（离线模式）');
        e.target.reset();
    }
}

function initScrollAnimations() {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    ['.section-header', '.product-card', '.about-content', '.about-image', '.value-card', '.contact-info', '.contact-form-container'].forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    fetchSettings();
    fetchProducts();
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => navbar.classList.toggle('scrolled', window.scrollY > 50));
    document.getElementById('navbarToggle')?.addEventListener('click', () => {
        document.querySelector('.navbar-menu')?.classList.toggle('active');
    });
    document.querySelectorAll('.nav-link').forEach(link => link.addEventListener('click', () => {
        document.querySelector('.navbar-menu')?.classList.remove('active');
    }));
});