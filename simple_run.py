from app import create_app, db

# Create a simple test app without authentication for now
def create_simple_app():
    from flask import Flask, render_template
    import os
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize only SQLAlchemy
    db.init_app(app)
    
    @app.route('/')
    def index():
        try:
            from app.models import Product, Category
            with app.app_context():
                featured_products = Product.query.filter_by(featured=True).limit(8).all()
                categories = Category.query.all()
        except:
            featured_products = []
            categories = []
        
        return render_template('index.html', 
                             featured_products=featured_products,
                             categories=categories)
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/contact')
    def contact():
        return render_template('contact.html')
    
    @app.route('/faq')
    def faq():
        return render_template('faq.html')
    
    return app

if __name__ == '__main__':
    app = create_simple_app()
    app.run(debug=True, port=5000)