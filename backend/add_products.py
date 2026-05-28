from app.database import SessionLocal
from app.models import Product

DEFAULT_PRODUCTS = [
    {
        "name": "天然竹筷套装",
        "category": "kitchen",
        "price": 29.90,
        "description": "精选优质楠竹，天然环保无添加。筷子光滑圆润，手感舒适，适合日常使用。套装包含10双筷子，满足家庭需求。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=premium%20bamboo%20chopsticks%20set%20elegant%20white%20background%20product%20photography%20minimalist%20style&image_size=square_hd",
        "specs": "材质: 优质楠竹\n数量: 10双/套\n长度: 24cm\n特点: 天然无漆"
    },
    {
        "name": "竹制砧板",
        "category": "kitchen",
        "price": 89.00,
        "description": "高密度竹材砧板，硬度高、耐用不易开裂。纹理清晰美观，分区设计生熟分离。清洗方便，抗菌防霉。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20cutting%20board%20kitchen%20utensil%20white%20background%20product%20photography%20clean%20minimalist&image_size=square_hd",
        "specs": "材质: 高密度竹材\n尺寸: 40×28×2cm\n特点: 生熟分离"
    },
    {
        "name": "竹制收纳盒三件套",
        "category": "home",
        "price": 68.00,
        "description": "简约时尚的竹制收纳盒套装，三种尺寸满足不同收纳需求。可用于收纳首饰、文具、化妆品等小物品，让生活更有条理。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20storage%20box%20organizer%20home%20decor%20white%20background%20product%20photography%20minimalist&image_size=square_hd",
        "specs": "材质: 楠竹\n数量: 3件套\n尺寸: 大中小三种规格\n颜色: 原竹色"
    },
    {
        "name": "竹制功夫茶盘",
        "category": "craft",
        "price": 158.00,
        "description": "传统工艺与现代设计相结合的电木茶盘。排水流畅，稳重大气，适合茶道爱好者使用。搭配茶具更显品味。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=elegant%20bamboo%20tea%20tray%20kung%20fu%20tea%20ceremony%20white%20background%20product%20photography&image_size=square_hd",
        "specs": "材质: 楠竹+电木\n尺寸: 45×25×4cm\n特点: 带排水系统"
    },
    {
        "name": "竹制桌面收纳架",
        "category": "office",
        "price": 78.00,
        "description": "多功能竹制桌面收纳架，可放置文件、书籍、手机等。分層设计，充分利用桌面空间，让办公环境更加整洁有序。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20desk%20organizer%20pen%20holder%20office%20supplies%20white%20background%20product%20photography&image_size=square_hd",
        "specs": "材质: 楠竹\n尺寸: 25×18×15cm\n层数: 3层\n用途: 文件、书籍收纳"
    },
    {
        "name": "竹制餐具套装",
        "category": "kitchen",
        "price": 59.00,
        "description": "健康环保的竹制餐具套装，包含碗、盘子、筷子。天然竹材，不含任何化学涂层，安全无毒。适合家庭日常使用。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20bowl%20set%20with%20chopsticks%20tableware%20white%20background%20product%20photography%20elegant&image_size=square_hd",
        "specs": "材质: 楠竹\n套装: 碗×4，盘子×4，筷子×4\n特点: 天然环保无漆"
    },
    {
        "name": "竹制纸巾盒",
        "category": "home",
        "price": 35.00,
        "description": "精美的竹制纸巾盒，造型简约大方。可放置抽纸或卷纸，适合客厅、卧室、卫生间等多种场景使用。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20tissue%20box%20holder%20bathroom%20accessory%20white%20background%20minimalist%20design&image_size=square_hd",
        "specs": "材质: 楠竹\n尺寸: 24×12×8cm\n特点: 适用于各种纸巾"
    },
    {
        "name": "竹制相框",
        "category": "craft",
        "price": 42.00,
        "description": "精致的竹制相框，可放置5寸照片。天然竹纹美观大方，可作为家居装饰或送礼佳品。支持横竖两种摆放方式。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20photo%20frame%20elegant%20home%20decor%20white%20background%20minimalist%20product%20photography&image_size=square_hd",
        "specs": "材质: 楠竹\n适用照片: 5寸（12.7×8.9cm）\n特点: 横竖两用"
    },
    {
        "name": "竹制笔筒",
        "category": "office",
        "price": 28.00,
        "description": "造型独特的竹制笔筒，可放置各种笔类、剪刀等办公文具。手工打磨，表面光滑细腻，是办公桌上的实用装饰品。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20pen%20holder%20desk%20organizer%20office%20supplies%20white%20background%20minimalist&image_size=square_hd",
        "specs": "材质: 楠竹\n尺寸: 8×8×10cm\n特点: 手工打磨"
    },
    {
        "name": "竹制果盘",
        "category": "home",
        "price": 55.00,
        "description": "典雅实用的竹制果盘，分层设计可同时摆放多种水果或零食。客厅待客必备，既美观又实用，提升家居品味。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20fruit%20bowl%20tray%20elegant%20home%20decor%20white%20background%20minimalist%20design&image_size=square_hd",
        "specs": "材质: 楠竹\n尺寸: 30×20×8cm\n特点: 分层设计"
    },
    {
        "name": "竹制置物架",
        "category": "home",
        "price": 128.00,
        "description": "多层竹制置物架，适用于浴室、厨房、阳台等多种场景。防水防潮，承重力强，安装简便，让空间利用更高效。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20shelving%20unit%20bathroom%20storage%20white%20background%20minimalist%20product%20photography&image_size=square_hd",
        "specs": "材质: 楠竹\n层数: 4层\n承重: 每层可承重15kg\n尺寸: 60×25×100cm"
    },
    {
        "name": "竹制首饰盒",
        "category": "craft",
        "price": 88.00,
        "description": "精致的竹制首饰盒，内设多个隔层，可分类存放戒指、耳环、项链等首饰。小巧精致，是存放珍贵饰品的好选择。",
        "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bamboo%20jewelry%20box%20elegant%20storage%20white%20background%20minimalist%20product%20photography&image_size=square_hd",
        "specs": "材质: 楠竹\n尺寸: 20×15×10cm\n特点: 多格分层设计"
    }
]

db = SessionLocal()

try:
    existing_count = db.query(Product).count()
    if existing_count > 0:
        print(f"数据库中已有 {existing_count} 个产品，跳过添加默认产品。")
    else:
        for product_data in DEFAULT_PRODUCTS:
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        print(f"✓ 成功添加 {len(DEFAULT_PRODUCTS)} 个默认产品！")
        
        print("\n产品列表：")
        for i, product in enumerate(DEFAULT_PRODUCTS, 1):
            print(f"{i}. {product['name']} - ¥{product['price']:.2f}")
    
finally:
    db.close()
