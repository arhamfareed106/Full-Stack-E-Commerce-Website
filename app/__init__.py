import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///shop.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Stripe configuration
    app.config['STRIPE_PUBLISHABLE_KEY'] = os.getenv('STRIPE_PUBLISHABLE_KEY')
    app.config['STRIPE_SECRET_KEY'] = os.getenv('STRIPE_SECRET_KEY')
    
    # Mail configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'localhost')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    
    # Upload configuration
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # Login manager setup
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    # from app.routes.auth import auth_bp
    # from app.routes.products import products_bp
    # from app.routes.cart import cart_bp
    # from app.routes.checkout import checkout_bp
    # from app.routes.admin import admin_bp
    # from app.routes.custom import custom_bp
    
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(products_bp)
    # app.register_blueprint(cart_bp, url_prefix='/cart')
    # app.register_blueprint(checkout_bp, url_prefix='/checkout')
    # app.register_blueprint(admin_bp, url_prefix='/admin')
    # app.register_blueprint(custom_bp, url_prefix='/custom')
    
    # Main routes
    @app.route('/')
    def index():
        from flask import render_template
        from app.models import Product, Category
        
        featured_products = Product.query.filter_by(featured=True).limit(8).all()
        categories = Category.query.all()
        
        return render_template('index.html', 
                             featured_products=featured_products,
                             categories=categories)
    
    @app.route('/about')
    def about():
        from flask import render_template
        return render_template('about.html')
    
    @app.route('/contact')
    def contact():
        from flask import render_template
        return render_template('contact.html')
    
    @app.route('/faq')
    def faq():
        from flask import render_template
        return render_template('faq.html')
    
    @app.route('/privacy')
    def privacy():
        from flask import render_template
        return render_template('privacy.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Create upload directory
    upload_dir = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_dir, exist_ok=True)
    
    return app