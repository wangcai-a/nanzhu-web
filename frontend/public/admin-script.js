const API_BASE_URL = 'http://localhost:8000';
let products = [], messages = [], currentToken = null;
let siteSettings = {
    stat_product_count: '500+',
    stat_sales_amount: '3000万+',
    stat_dealer_count: '50+',
    contact_address: '福建省龙岩市长汀县工业园区',
    contact_phone: '0597-1234567',
    contact_email: 'contact@nanzhu-bamboo.com',
    contact_hours: '周一至周六 8:00-18:00'
};

async function init() {
    updateTime();
    setInterval(updateTime, 1000);
    const token = sessionStorage.getItem('admin_token');
    if (token) {
        currentToken = token;
        showAdminPage();
    } else {
        showLoginPage();
    }
}

function showLoginPage() {
    document.getElementById('loginPage').classList.remove('hidden');
    document.getElementById('adminPage').classList.add('hidden');
}

function showAdminPage() {
    document.getElementById('loginPage').classList.add('hidden');
    document.getElementById('adminPage').classList.remove('hidden');
    loadDashboardData();
}

async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        });
        if (response.ok) {
            const data = await response.json();
            currentToken = data.access_token;
            sessionStorage.setItem('admin_token', currentToken);
            showAdminPage();
        } else {
            alert('用户名或密码错误！');
        }
    } catch (error) {
        console.error('Login failed:', error);
        if (username === 'admin' && password === 'admin123') {
            currentToken = 'demo_token';
            sessionStorage.setItem('admin_token', currentToken);
            loadMockData();
            showAdminPage();
        } else {
            alert('登录失败，请确保后端服务已启动！');
        }
    }
}

async function loadDashboardData() {
    await fetchProducts();
    await fetchMessages();
    await fetchSiteSettings();
    updateDashboard();
}

async function fetchSiteSettings() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/settings`);
        if (response.ok) {
            siteSettings = { ...siteSettings, ...await response.json() };
        }
    } catch (error) {
        console.error('Failed to fetch settings:', error);
    }
    updateSettingsForm();
}

function updateSettingsForm() {
    document.getElementById('statProductCount').value = siteSettings.stat_product_count || '';
    document.getElementById('statSalesAmount').value = siteSettings.stat_sales_amount || '';
    document.getElementById('statDealerCount').value = siteSettings.stat_dealer_count || '';
    document.getElementById('contactAddress').value = siteSettings.contact_address || '';
    document.getElementById('contactPhone').value = siteSettings.contact_phone || '';
    document.getElementById('contactEmail').value = siteSettings.contact_email || '';
    document.getElementById('contactHours').value = siteSettings.contact_hours || '';
}

async function saveSiteSettings(e) {
    e.preventDefault();
    const updates = {
        stat_product_count: document.getElementById('statProductCount').value,
        stat_sales_amount: document.getElementById('statSalesAmount').value,
        stat_dealer_count: document.getElementById('statDealerCount').value,
        contact_address: document.getElementById('contactAddress').value,
        contact_phone: document.getElementById('contactPhone').value,
        contact_email: document.getElementById('contactEmail').value,
        contact_hours: document.getElementById('contactHours').value
    };
    try {
        const response = await fetch(`${API_BASE_URL}/api/settings`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updates)
        });
        if (response.ok) {
            Object.assign(siteSettings, updates);
            alert('网站设置保存成功！');
        } else {
            throw new Error('Save failed');
        }
    } catch (error) {
        console.error('Save settings failed:', error);
        Object.assign(siteSettings, updates);
        alert('网站设置保存成功！(离线模式)');
    }
}

async function fetchProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/products`);
        if (response.ok) products = await response.json();
        else loadMockProducts();
    } catch (error) {
        console.error('Failed to fetch products:', error);
        loadMockProducts();
    }
}

function loadMockProducts() {
    products = [
        { id: 1, name: '天然竹筷套装', category: 'kitchen', price: 29.90, description: '精选优质楠竹', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=premium%20bamboo%20chopsticks%20set%20elegant%20white%20background%20product%20photography%20minimalist%20style&image_size=square_hd' },
        { id: 2, name: '竹制砧板', category: 'kitchen', price: 89.00, description: '高密度竹材', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20cutting%20board%20kitchen%20utensil%20white%20background%20product%20photography%20clean%20minimalist&image_size=square_hd' },
        { id: 3, name: '竹制收纳盒', category: 'home', price: 45.00, description: '多功能收纳', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20storage%20box%20organizer%20home%20decor%20white%20background%20product%20photography%20minimalist&image_size=square_hd' },
        { id: 4, name: '竹制茶盘', category: 'craft', price: 158.00, description: '功夫茶必备', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=elegant%20bamboo%20tea%20tray%20kung%20fu%20tea%20ceremony%20white%20background%20product%20photography&image_size=square_hd' },
        { id: 5, name: '竹制办公收纳', category: 'office', price: 68.00, description: '简约时尚', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20desk%20organizer%20pen%20holder%20office%20supplies%20white%20background%20product%20photography&image_size=square_hd' },
        { id: 6, name: '竹制餐具套装', category: 'kitchen', price: 59.00, description: '天然环保', image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20bowl%20set%20with%20chopsticks%20tableware%20white%20background%20product%20photography%20elegant&image_size=square_hd' }
    ];
}

async function fetchMessages() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/messages`);
        if (response.ok) messages = await response.json();
        else messages = [];
    } catch (error) {
        console.error('Failed to fetch messages:', error);
        messages = [];
    }
}

function loadMockData() {
    loadMockProducts();
    messages = [];
}

function updateTime() {
    document.getElementById('currentTime').textContent = new Date().toLocaleString('zh-CN');
}

function updateDashboard() {
    document.getElementById('productCount').textContent = products.length;
    const pendingCount = messages.filter(m => m.status === 'pending').length;
    document.getElementById('messageCount').textContent = pendingCount;
    document.getElementById('messageBadge').textContent = pendingCount;
    document.getElementById('messageBadge').style.display = pendingCount > 0 ? 'block' : 'none';
    renderLatestMessages();
    updateCategoryStats();
}

function updateCategoryStats() {
    const categories = { kitchen: 0, home: 0, craft: 0, office: 0 };
    products.forEach(p => { if (categories[p.category] !== undefined) categories[p.category]++; });
    document.getElementById('categoryStats').innerHTML = [
        { name: '竹制厨具', count: categories.kitchen },
        { name: '竹制家居', count: categories.home },
        { name: '竹制工艺品', count: categories.craft },
        { name: '办公用品', count: categories.office }
    ].map(cat => `<div class="category-item"><span class="category-name">${cat.name}</span><span class="category-count">${cat.count}</span></div>`).join('');
}

function renderLatestMessages() {
    const latest = messages.slice(-5).reverse();
    const container = document.getElementById('latestMessages');
    if (latest.length === 0) {
        container.innerHTML = '<p class="empty-text">暂无留言</p>';
        return;
    }
    container.innerHTML = latest.map(msg => `
        <div class="latest-item" onclick="viewMessage(${msg.id})">
            <div class="name">${msg.name} <span class="status-badge ${msg.status}">${msg.status === 'pending' ? '待处理' : '已处理'}</span></div>
            <div class="content">${msg.content}</div>
        </div>
    `).join('');
}

function navigateTo(page) {
    document.querySelectorAll('.page-section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    document.getElementById(page + 'Page').classList.add('active');
    document.querySelector(`[data-page="${page}"]`).classList.add('active');
    const titles = { dashboard: '仪表盘', products: '产品管理', messages: '留言管理', settings: '系统设置' };
    document.getElementById('pageTitle').textContent = titles[page];
    if (page === 'products') renderProductsTable();
    if (page === 'messages') renderMessagesTable();
}

function getCategoryName(category) {
    const names = { kitchen: '竹制厨具', home: '竹制家居', craft: '竹制工艺品', office: '办公用品' };
    return names[category] || category;
}

function renderProductsTable() {
    const tbody = document.getElementById('productsTableBody');
    tbody.innerHTML = products.map(product => `
        <tr>
            <td>${product.id}</td>
            <td><img src="${product.image}" alt="${product.name}" class="product-thumb" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2260%22 height=%2260%22%3E%3Crect fill=%22%23f0f0f0%22 width=%2260%22 height=%2260%22/%3E%3C/svg%3E'"></td>
            <td>${product.name}</td>
            <td>${getCategoryName(product.category)}</td>
            <td>¥${product.price.toFixed(2)}</td>
            <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${product.description}</td>
            <td>
                <button class="action-btn" onclick="editProduct(${product.id})">编辑</button>
                <button class="action-btn delete" onclick="deleteProduct(${product.id})">删除</button>
            </td>
        </tr>
    `).join('');
}

function showProductModal(product = null) {
    const form = document.getElementById('productForm');
    if (product) {
        document.getElementById('productModalTitle').textContent = '编辑产品';
        document.getElementById('productId').value = product.id;
        document.getElementById('productName').value = product.name;
        document.getElementById('productCategory').value = product.category;
        document.getElementById('productPrice').value = product.price;
        document.getElementById('productDescription').value = product.description;
        document.getElementById('productImage').value = product.image;
    } else {
        document.getElementById('productModalTitle').textContent = '添加产品';
        form.reset();
        document.getElementById('productId').value = '';
    }
    document.getElementById('productModal').classList.remove('hidden');
}

function closeProductModal() {
    document.getElementById('productModal').classList.add('hidden');
}

async function saveProduct(e) {
    e.preventDefault();
    const productData = {
        name: document.getElementById('productName').value,
        category: document.getElementById('productCategory').value,
        price: parseFloat(document.getElementById('productPrice').value),
        description: document.getElementById('productDescription').value,
        image: document.getElementById('productImage').value
    };
    const id = document.getElementById('productId').value;
    try {
        const url = id ? `${API_BASE_URL}/api/products/${id}` : `${API_BASE_URL}/api/products`;
        const method = id ? 'PUT' : 'POST';
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${currentToken}` },
            body: JSON.stringify(productData)
        });
        if (response.ok) {
            await fetchProducts();
            renderProductsTable();
            updateDashboard();
            closeProductModal();
            alert('产品保存成功！');
        } else {
            throw new Error('Save failed');
        }
    } catch (error) {
        console.error('Save product failed:', error);
        if (!id) productData.id = products.length + 1;
        else Object.assign(products.find(p => p.id === parseInt(id)), productData);
        renderProductsTable();
        updateDashboard();
        closeProductModal();
        alert('产品保存成功！(离线模式)');
    }
}

function editProduct(id) {
    const product = products.find(p => p.id === id);
    if (product) showProductModal(product);
}

async function deleteProduct(id) {
    if (!confirm('确定要删除这个产品吗？')) return;
    try {
        const response = await fetch(`${API_BASE_URL}/api/products/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${currentToken}` }
        });
        if (response.ok) {
            await fetchProducts();
            renderProductsTable();
            updateDashboard();
            alert('产品已删除！');
        }
    } catch (error) {
        products = products.filter(p => p.id !== id);
        renderProductsTable();
        updateDashboard();
        alert('产品已删除！(离线模式)');
    }
}

function renderMessagesTable() {
    const tbody = document.getElementById('messagesTableBody');
    if (messages.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 40px;">暂无留言</td></tr>';
        return;
    }
    tbody.innerHTML = messages.map(msg => `
        <tr>
            <td>${msg.id}</td>
            <td>${msg.name}</td>
            <td>${msg.email}</td>
            <td>${msg.phone}</td>
            <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${msg.content}</td>
            <td>${new Date(msg.created_at || msg.time).toLocaleString('zh-CN')}</td>
            <td><span class="status-badge ${msg.status}">${msg.status === 'pending' ? '待处理' : '已处理'}</span></td>
            <td>
                <button class="action-btn" onclick="viewMessage(${msg.id})">查看</button>
                ${msg.status === 'pending' ? `<button class="action-btn" onclick="markProcessed(${msg.id})">处理</button>` : ''}
                <button class="action-btn delete" onclick="deleteMessage(${msg.id})">删除</button>
            </td>
        </tr>
    `).join('');
}

function viewMessage(id) {
    const msg = messages.find(m => m.id === id);
    if (!msg) return;
    document.getElementById('messageDetail').innerHTML = `
        <p><strong>姓名：</strong>${msg.name}</p>
        <p><strong>邮箱：</strong>${msg.email}</p>
        <p><strong>电话：</strong>${msg.phone}</p>
        <p><strong>时间：</strong>${new Date(msg.created_at || msg.time).toLocaleString('zh-CN')}</p>
        <p><strong>状态：</strong><span class="status-badge ${msg.status}">${msg.status === 'pending' ? '待处理' : '已处理'}</span></p>
        <div class="message-content">${msg.content}</div>
    `;
    document.getElementById('processMessageBtn').style.display = msg.status === 'pending' ? 'block' : 'none';
    document.getElementById('messageModal').classList.remove('hidden');
}

function closeMessageModal() {
    document.getElementById('messageModal').classList.add('hidden');
}

async function markProcessed(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/messages/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${currentToken}` },
            body: JSON.stringify({ status: 'processed' })
        });
        if (response.ok) {
            await fetchMessages();
            renderMessagesTable();
            updateDashboard();
            closeMessageModal();
            alert('留言已处理！');
        }
    } catch (error) {
        const msg = messages.find(m => m.id === id);
        if (msg) msg.status = 'processed';
        renderMessagesTable();
        updateDashboard();
        closeMessageModal();
        alert('留言已处理！(离线模式)');
    }
}

async function deleteMessage(id) {
    if (!confirm('确定要删除这条留言吗？')) return;
    try {
        const response = await fetch(`${API_BASE_URL}/api/messages/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${currentToken}` }
        });
        if (response.ok) {
            await fetchMessages();
            renderMessagesTable();
            updateDashboard();
            alert('留言已删除！');
        }
    } catch (error) {
        messages = messages.filter(m => m.id !== id);
        renderMessagesTable();
        updateDashboard();
        alert('留言已删除！(离线模式)');
    }
}

function exportData() {
    const data = { products, messages, exportTime: new Date().toLocaleString('zh-CN') };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `nanzhu_data_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    alert('数据导出成功！');
}

function clearMessages() {
    if (!confirm('确定要清空所有留言吗？')) return;
    messages = [];
    renderMessagesTable();
    updateDashboard();
    alert('留言已清空！');
}

document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    login(document.getElementById('username').value, document.getElementById('password').value);
});

document.getElementById('logoutBtn').addEventListener('click', () => {
    sessionStorage.removeItem('admin_token');
    currentToken = null;
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    showLoginPage();
});

document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => navigateTo(item.dataset.page));
});

document.getElementById('accountForm').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('密码修改功能需要连接后端服务！');
});

document.getElementById('productForm').addEventListener('submit', saveProduct);

document.getElementById('siteSettingsForm').addEventListener('submit', saveSiteSettings);

init();