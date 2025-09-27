# PatchCraft E-Commerce - Deployment Guide

## 🚀 Quick Start (Current Working Version)

The application is currently running in a simplified mode due to Python dependency compatibility issues. Here's how to get it working:

### Running the Test Version
```bash
# 1. Navigate to project directory
cd "f:\coding\company project\clone project"

# 2. Activate virtual environment
.\venv\Scripts\activate

# 3. Run the test server
python test_app.py
```

The app will be available at: http://localhost:5000

## 📁 Project Structure

```
patchcraft/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── forms.py             # WTForms definitions
│   ├── routes/              # Blueprint routes
│   │   ├── auth.py          # Authentication (commented out)
│   │   ├── products.py      # Product catalog
│   │   ├── cart.py          # Shopping cart
│   │   ├── checkout.py      # Payment processing
│   │   ├── admin.py         # Admin dashboard
│   │   └── custom.py        # Custom orders
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html        # Base template
│   │   ├── index.html       # Homepage
│   │   ├── about.html       # About page
│   │   ├── contact.html     # Contact page
│   │   ├── faq.html         # FAQ page
│   │   ├── auth/            # Authentication templates
│   │   ├── cart/            # Cart templates
│   │   ├── products/        # Product templates
│   │   └── custom/          # Custom order templates
│   └── static/              # CSS, JS, images
│       ├── css/
│       │   ├── input.css    # Tailwind source
│       │   └── tailwind.css # Compiled CSS
│       ├── images/
│       └── uploads/
├── migrations/              # Database migrations
├── venv/                   # Virtual environment
├── .env                    # Environment variables
├── .env.example           # Environment template
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies
├── tailwind.config.js    # Tailwind configuration
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose
├── nginx.conf            # Nginx configuration
├── run.py               # Main application entry
├── test_app.py          # Working test version
├── init_db.py           # Database initialization
└── README.md            # This file
```

## 🔧 Features Implemented

### ✅ Working Features
- **Homepage**: Hero section with featured products and categories
- **Product Display**: Sample products and categories
- **Static Pages**: About, Contact, FAQ pages
- **Database**: SQLite with sample data
- **Responsive Design**: Tailwind CSS styling
- **Basic Structure**: Complete MVC architecture

### 🚧 Features Ready (Need Dependency Fix)
- **User Authentication**: Login, registration, user profiles
- **Shopping Cart**: Session-based cart management
- **Product Catalog**: Full product browsing with search and filters
- **Admin Dashboard**: Product and order management
- **Custom Orders**: File upload and custom order requests
- **Stripe Integration**: Payment processing setup
- **Email Notifications**: Mail integration configured

## 🛠️ Known Issues & Solutions

### Issue 1: Flask-Login Compatibility
**Problem**: `ImportError: cannot import name 'url_decode' from 'werkzeug.urls'`

**Temporary Solution**: Authentication features are commented out in the test version.

**Permanent Solution**: 
```bash
# Try these compatible versions:
pip install Flask==2.3.2 Flask-Login==0.6.1 Werkzeug==2.3.6
# OR upgrade to newer compatible versions:
pip install Flask==3.0.0 Flask-Login==0.6.3 Werkzeug==3.0.0
```

### Issue 2: Missing Templates
Some advanced templates need completion. The basic structure is in place.

## 🚀 Production Deployment

### Method 1: Docker (Recommended)
```bash
# 1. Fix dependency issues first
# 2. Build and run with Docker
docker-compose up --build
```

### Method 2: Traditional Deployment
```bash
# 1. Set up production environment variables
cp .env.example .env
# Edit .env with production values

# 2. Install dependencies
pip install -r requirements.txt
npm install
npm run build-css

# 3. Initialize database
python init_db.py

# 4. Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 run:app
```

## 🎨 Customization Guide

### Styling
- **Colors**: Modify `tailwind.config.js` for custom color schemes
- **Components**: Update `app/static/css/input.css` for custom styles
- **Rebuild**: Run `npm run build-css` after changes

### Content
- **Branding**: Update "PatchCraft" in templates and configurations
- **Images**: Add product images to `app/static/images/products/`
- **Text**: Modify templates in `app/templates/`

### Database
- **Products**: Add more sample data in `init_db.py`
- **Schema**: Modify models in `app/models.py`
- **Migrations**: Use Flask-Migrate for schema changes

## 📧 Configuration

### Environment Variables (.env)
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///shop.db
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Stripe Setup
1. Create account at https://stripe.com
2. Get API keys from dashboard
3. Add to .env file
4. Test with test keys first

## 🏗️ Next Steps for Full Functionality

1. **Fix Dependencies**: Resolve Flask-Login compatibility
2. **Complete Templates**: Finish all template files
3. **Test Authentication**: Verify login/registration works
4. **Implement Cart**: Enable shopping cart functionality
5. **Add Products**: Create more sample products
6. **Configure Stripe**: Set up payment processing
7. **Email Setup**: Configure email notifications
8. **Admin Panel**: Complete admin functionality

## 🆘 Troubleshooting

### Common Issues
1. **Import Errors**: Check virtual environment activation
2. **Template Not Found**: Verify template paths
3. **CSS Not Loading**: Run `npm run build-css`
4. **Database Errors**: Run `python init_db.py`

### Support
For issues or questions:
- Check error logs in terminal
- Verify file paths are correct
- Ensure all dependencies are installed
- Test with minimal configuration first

## 📄 License
This project is created for educational/commercial use. Feel free to modify and distribute.