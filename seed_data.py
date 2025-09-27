#!/usr/bin/env python
"""
Seed script to populate the database with sample data
"""
import os
import sys

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Category, Product

def seed_data():
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
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
        
        # Create sample user
        sample_user = User.query.filter_by(email='user@example.com').first()
        if not sample_user:
            sample_user = User(
                email='user@example.com',
                first_name='John',
                last_name='Doe'
            )
            sample_user.set_password('password123')
            db.session.add(sample_user)
        
        # Create categories
        categories_data = [
            {
                'name': 'Patches',
                'slug': 'patches',
                'description': 'Custom embroidered patches for uniforms, jackets, and more'
            },
            {
                'name': 'Apparel',
                'slug': 'apparel',
                'description': 'Custom clothing and uniforms with your designs'
            },
            {
                'name': 'Accessories',
                'slug': 'accessories',
                'description': 'Keychains, pins, and other custom accessories'
            },
            {
                'name': 'Badges',
                'slug': 'badges',
                'description': 'Professional badges and name tags'
            }
        ]
        
        for cat_data in categories_data:
            category = Category.query.filter_by(slug=cat_data['slug']).first()
            if not category:
                category = Category(**cat_data)
                db.session.add(category)
        
        db.session.commit()
        
        # Create sample products
        patches_cat = Category.query.filter_by(slug='patches').first()
        apparel_cat = Category.query.filter_by(slug='apparel').first()
        accessories_cat = Category.query.filter_by(slug='accessories').first()
        badges_cat = Category.query.filter_by(slug='badges').first()
        
        products_data = [
            # Patches
            {
                'name': 'Custom Logo Patch',
                'slug': 'custom-logo-patch',
                'description': 'High-quality embroidered patch with your custom logo. Perfect for uniforms, jackets, and bags.',
                'price': 8.99,
                'stock': 100,
                'category_id': patches_cat.id,
                'featured': True,
                'image': 'logo-patch.jpg'
            },
            {
                'name': 'Team Name Patch',
                'slug': 'team-name-patch',
                'description': 'Professional team name patches with custom colors and fonts.',
                'price': 6.99,
                'stock': 150,
                'category_id': patches_cat.id,
                'featured': True,
                'image': 'team-patch.jpg'
            },
            {
                'name': 'Round Morale Patch',
                'slug': 'round-morale-patch',
                'description': 'Durable round patches perfect for military, law enforcement, and outdoor gear.',
                'price': 12.99,
                'stock': 75,
                'category_id': patches_cat.id,
                'featured': True,
                'image': 'morale-patch.jpg'
            },
            
            # Apparel
            {
                'name': 'Custom Polo Shirt',
                'slug': 'custom-polo-shirt',
                'description': 'Professional polo shirt with custom embroidery. Available in multiple colors.',
                'price': 29.99,
                'stock': 50,
                'category_id': apparel_cat.id,
                'featured': True,
                'image': 'polo-shirt.jpg'
            },
            {
                'name': 'Embroidered Baseball Cap',
                'slug': 'embroidered-baseball-cap',
                'description': 'Classic baseball cap with custom embroidered logo or text.',
                'price': 19.99,
                'stock': 80,
                'category_id': apparel_cat.id,
                'featured': True,
                'image': 'baseball-cap.jpg'
            },
            {
                'name': 'Custom T-Shirt',
                'slug': 'custom-t-shirt',
                'description': 'Comfortable cotton t-shirt with screen printed or embroidered designs.',
                'price': 24.99,
                'stock': 120,
                'category_id': apparel_cat.id,
                'featured': True,
                'image': 't-shirt.jpg'
            },
            
            # Accessories
            {
                'name': 'Custom Keychain',
                'slug': 'custom-keychain',
                'description': 'Durable embroidered keychain with your logo or design.',
                'price': 4.99,
                'stock': 200,
                'category_id': accessories_cat.id,
                'featured': True,
                'image': 'keychain.jpg'
            },
            {
                'name': 'Enamel Pin',
                'slug': 'enamel-pin',
                'description': 'High-quality enamel pin with custom design and colors.',
                'price': 7.99,
                'stock': 150,
                'category_id': accessories_cat.id,
                'featured': True,
                'image': 'enamel-pin.jpg'
            },
            
            # Badges
            {
                'name': 'Name Badge',
                'slug': 'name-badge',
                'description': 'Professional name badge with custom text and logo.',
                'price': 9.99,
                'stock': 100,
                'category_id': badges_cat.id,
                'image': 'name-badge.jpg'
            },
            {
                'name': 'ID Badge',
                'slug': 'id-badge',
                'description': 'Security ID badge with photo and custom information.',
                'price': 14.99,
                'stock': 60,
                'category_id': badges_cat.id,
                'image': 'id-badge.jpg'
            }
        ]
        
        for prod_data in products_data:
            product = Product.query.filter_by(slug=prod_data['slug']).first()
            if not product:
                product = Product(**prod_data)
                db.session.add(product)
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()