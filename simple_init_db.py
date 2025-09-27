import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

# Create a simple Flask app just for database initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath("shop.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define models directly here to avoid import issues
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    image = db.Column(db.String(200))
    featured = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

if __name__ == '__main__':
    print("Initializing database...")
    print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Current directory: {os.getcwd()}")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created!")
        
        # Create admin user
        admin_user = User.query.filter_by(email='admin@patchcraft.com').first()
        if not admin_user:
            admin_user = User(
                email='admin@patchcraft.com',
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("✓ Admin user created!")
        else:
            print("✓ Admin user already exists")
        
        # Create sample category
        patches_cat = Category.query.filter_by(slug='patches').first()
        if not patches_cat:
            patches_cat = Category(
                name='Patches',
                slug='patches',
                description='Custom embroidered patches'
            )
            db.session.add(patches_cat)
            db.session.commit()
            print("✓ Sample category created!")
        else:
            print("✓ Sample category already exists")
        
        # Create sample product
        sample_product = Product.query.filter_by(slug='custom-logo-patch').first()
        if not sample_product:
            sample_product = Product(
                name='Custom Logo Patch',
                slug='custom-logo-patch',
                description='High-quality embroidered patch with your custom logo.',
                price=8.99,
                stock=100,
                category_id=patches_cat.id,
                featured=True
            )
            db.session.add(sample_product)
            db.session.commit()
            print("✓ Sample product created!")
        else:
            print("✓ Sample product already exists")
        
        print("✓ Database initialization complete!")
        
        # Verify database was created
        if os.path.exists('shop.db'):
            print("✓ Database file confirmed to exist")
        else:
            print("✗ Database file not found after creation")