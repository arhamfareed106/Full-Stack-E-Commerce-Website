import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import CustomOrder
from app.forms import CustomOrderForm

custom_bp = Blueprint('custom', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ai', 'psd'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@custom_bp.route('/order', methods=['GET', 'POST'])
@login_required
def custom_order():
    form = CustomOrderForm()
    
    if form.validate_on_submit():
        # Handle file upload
        file_path = None
        if form.design_file.data:
            file = form.design_file.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                file_path = f'uploads/{filename}'  # Store relative path
            else:
                flash('Invalid file type. Please upload JPG, PNG, PDF, AI, or PSD files.', 'error')
                return render_template('custom/order_form.html', form=form)
        
        # Create custom order
        custom_order = CustomOrder(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            file_path=file_path,
            notes=form.notes.data,
            status='pending'
        )
        
        db.session.add(custom_order)
        db.session.commit()
        
        flash('Custom order submitted successfully! We will review it and get back to you soon.', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('custom/order_form.html', form=form)

@custom_bp.route('/orders')
@login_required
def my_orders():
    custom_orders = CustomOrder.query.filter_by(user_id=current_user.id).order_by(
        CustomOrder.created_at.desc()
    ).all()
    
    return render_template('custom/my_orders.html', custom_orders=custom_orders)

@custom_bp.route('/orders/<int:id>')
@login_required
def order_detail(id):
    custom_order = CustomOrder.query.filter_by(
        id=id, 
        user_id=current_user.id
    ).first_or_404()
    
    return render_template('custom/order_detail.html', custom_order=custom_order)