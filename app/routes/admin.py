import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Product, Category, Order, CustomOrder
from app.forms import ProductForm, CategoryForm, AdminCustomOrderForm
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    # Get dashboard statistics
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         recent_orders=recent_orders)

@admin_bp.route('/products')
@login_required
@admin_required
def products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        # Handle image upload
        image_filename = None
        if form.image.data:
            image_file = form.image.data
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.root_path, 'static', 'images', 'products', image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image_file.save(image_path)
        
        product = Product(
            name=form.name.data,
            slug=form.slug.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data,
            image=image_filename,
            featured=form.featured.data,
            active=form.active.data
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/add_product.html', form=form)

@admin_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        # Handle image upload
        if form.image.data:
            image_file = form.image.data
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.root_path, 'static', 'images', 'products', image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image_file.save(image_path)
            product.image = image_filename
        
        product.name = form.name.data
        product.slug = form.slug.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data
        product.featured = form.featured.data
        product.active = form.active.data
        
        db.session.commit()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/edit_product.html', form=form, product=product)

@admin_bp.route('/products/delete/<int:id>')
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.products'))

@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            slug=form.slug.data,
            description=form.description.data
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Category added successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/add_category.html', form=form)

@admin_bp.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = form.slug.data
        category.description = form.description.data
        
        db.session.commit()
        
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/edit_category.html', form=form, category=category)

@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/orders/<int:id>')
@login_required
@admin_required
def order_detail(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/orders/<int:id>/update_status', methods=['POST'])
@login_required
@admin_required
def update_order_status(id):
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'paid', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash('Order status updated successfully!', 'success')
    else:
        flash('Invalid status.', 'error')
    
    return redirect(url_for('admin.order_detail', id=id))

@admin_bp.route('/custom-orders')
@login_required
@admin_required
def custom_orders():
    page = request.args.get('page', 1, type=int)
    custom_orders = CustomOrder.query.order_by(CustomOrder.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/custom_orders.html', custom_orders=custom_orders)

@admin_bp.route('/custom-orders/<int:id>')
@login_required
@admin_required
def custom_order_detail(id):
    custom_order = CustomOrder.query.get_or_404(id)
    form = AdminCustomOrderForm(obj=custom_order)
    
    return render_template('admin/custom_order_detail.html', 
                         custom_order=custom_order, 
                         form=form)

@admin_bp.route('/custom-orders/<int:id>/update', methods=['POST'])
@login_required
@admin_required
def update_custom_order(id):
    custom_order = CustomOrder.query.get_or_404(id)
    form = AdminCustomOrderForm()
    
    if form.validate_on_submit():
        custom_order.status = form.status.data
        custom_order.estimated_price = form.estimated_price.data
        custom_order.final_price = form.final_price.data
        custom_order.admin_notes = form.admin_notes.data
        
        db.session.commit()
        
        flash('Custom order updated successfully!', 'success')
        return redirect(url_for('admin.custom_order_detail', id=id))
    
    return render_template('admin/custom_order_detail.html', 
                         custom_order=custom_order, 
                         form=form)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/users.html', users=users)