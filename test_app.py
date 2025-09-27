from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# Create standalone test app
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html', featured_products=[], categories=[])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# Add missing product routes
@app.route('/products')
def list_products():
    return "<h1>Products Page</h1><p>Product listing will be implemented here.</p>"

@app.route('/product/<slug>')
def product_detail(slug):
    return f"<h1>Product: {slug}</h1><p>Product details will be implemented here.</p>"

@app.route('/category/<slug>')
def category_products(slug):
    return f"<h1>Category: {slug}</h1><p>Category products will be implemented here.</p>"

@app.route('/search')
def search():
    return "<h1>Search</h1><p>Search functionality will be implemented here.</p>"

# Add missing cart routes
@app.route('/cart')
def view_cart():
    return "<h1>Shopping Cart</h1><p>Shopping cart will be implemented here.</p>"

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    return "Item added to cart"

@app.route('/cart/update', methods=['POST'])
def update_cart():
    return "Cart updated"

@app.route('/cart/clear')
def clear_cart():
    return "Cart cleared"

# Add missing checkout routes
@app.route('/checkout')
def checkout():
    return "<h1>Checkout</h1><p>Checkout process will be implemented here.</p>"

# Add missing auth routes
@app.route('/auth/login')
def login():
    return "<h1>Login</h1><p>Login form will be implemented here.</p>"

@app.route('/auth/register')
def register():
    return "<h1>Register</h1><p>Registration form will be implemented here.</p>"

@app.route('/auth/logout')
def logout():
    return "<h1>Logout</h1><p>You have been logged out.</p>"

@app.route('/auth/profile')
def profile():
    return "<h1>Profile</h1><p>User profile will be implemented here.</p>"

# Add missing custom order routes
@app.route('/custom/order')
def custom_order():
    return "<h1>Custom Order</h1><p>Custom order form will be implemented here.</p>"

@app.route('/custom/orders')
def my_orders():
    return "<h1>My Custom Orders</h1><p>Order history will be implemented here.</p>"

# Add missing admin routes
@app.route('/admin')
def admin_dashboard():
    return "<h1>Admin Dashboard</h1><p>Admin functionality will be implemented here.</p>"

# Context processor to provide cart data to templates
@app.context_processor
def inject_cart_data():
    return {
        'cart_count': 0,
        'cart_total': 0,
        'current_user': type('obj', (object,), {'is_authenticated': False, 'is_admin': False})()
    }

if __name__ == '__main__':
    print("Starting simple Flask server...")
    print("Visit: http://localhost:5000")
    app.run(debug=True, port=5000)