from app import create_app, db
from app import create_app, db
import os

app = create_app()
print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
print(f"Current directory: {os.getcwd()}")

if __name__ == '__main__':
    with app.app_context():
        # Import models to ensure they are registered
        from app.models import User, Category, Product, Order, OrderItem, CustomOrder
        
        # Create all tables
        db.create_all()
        print("Database tables created!")
        
        # Create admin user if not exists
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
            print("Admin user created!")
        
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
            print("Sample category created!")
        
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
            print("Sample product created!")
        
        print("Database initialization complete!")