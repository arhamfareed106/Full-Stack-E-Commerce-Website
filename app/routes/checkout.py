import stripe
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, Order, OrderItem
from app.forms import CheckoutForm
from app.routes.cart import get_cart, get_cart_total, save_cart

checkout_bp = Blueprint('checkout', __name__)

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@checkout_bp.route('/')
@login_required
def checkout():
    cart = get_cart()
    
    if not cart:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('cart.view_cart'))
    
    # Get cart items with product details
    cart_items = []
    total = 0
    
    for product_id, item_data in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            # Check stock availability
            if product.stock < item_data['quantity']:
                flash(f'Sorry, only {product.stock} of {product.name} available.', 'error')
                return redirect(url_for('cart.view_cart'))
            
            item_total = product.price * item_data['quantity']
            cart_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'total': item_total
            })
            total += item_total
    
    form = CheckoutForm()
    
    # Pre-fill form with user data
    if current_user.is_authenticated:
        form.billing_first_name.data = current_user.first_name
        form.billing_last_name.data = current_user.last_name
        form.billing_email.data = current_user.email
    
    return render_template('checkout/checkout.html', 
                         cart_items=cart_items, 
                         total=total, 
                         form=form,
                         stripe_public_key=current_app.config['STRIPE_PUBLISHABLE_KEY'])

@checkout_bp.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment_intent():
    try:
        cart = get_cart()
        if not cart:
            return jsonify({'error': 'Cart is empty'}), 400
        
        total = get_cart_total()
        
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Stripe expects cents
            currency='usd',
            metadata={
                'user_id': current_user.id,
                'cart_items': str(len(cart))
            }
        )
        
        return jsonify({
            'client_secret': intent.client_secret
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@checkout_bp.route('/process', methods=['POST'])
@login_required
def process_checkout():
    form = CheckoutForm()
    
    if form.validate_on_submit():
        cart = get_cart()
        
        if not cart:
            flash('Your cart is empty.', 'error')
            return redirect(url_for('cart.view_cart'))
        
        try:
            # Create order in database
            order = Order(
                user_id=current_user.id,
                total_price=get_cart_total(),
                status='pending',
                billing_address=f"{form.billing_address.data}, {form.billing_city.data}, {form.billing_state.data} {form.billing_zip.data}, {form.billing_country.data}",
                shipping_address=f"{form.shipping_address.data or form.billing_address.data}, {form.shipping_city.data or form.billing_city.data}, {form.shipping_state.data or form.billing_state.data} {form.shipping_zip.data or form.billing_zip.data}, {form.shipping_country.data or form.billing_country.data}"
            )
            
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Add order items
            for product_id, item_data in cart.items():
                product = Product.query.get(int(product_id))
                if product:
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=item_data['quantity'],
                        price=product.price
                    )
                    db.session.add(order_item)
                    
                    # Update product stock
                    product.stock -= item_data['quantity']
            
            # Create Stripe checkout session
            line_items = []
            for product_id, item_data in cart.items():
                product = Product.query.get(int(product_id))
                if product:
                    line_items.append({
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': product.name,
                                'images': [product.image_url] if product.image else [],
                            },
                            'unit_amount': int(product.price * 100),
                        },
                        'quantity': item_data['quantity'],
                    })
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=url_for('checkout.success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('checkout.cancel', _external=True),
                metadata={
                    'order_id': order.id,
                    'user_id': current_user.id
                }
            )
            
            # Store checkout session ID
            order.stripe_payment_intent_id = checkout_session.id
            db.session.commit()
            
            return redirect(checkout_session.url, code=303)
            
        except stripe.error.StripeError as e:
            db.session.rollback()
            flash(f'Payment error: {str(e)}', 'error')
            return redirect(url_for('checkout.checkout'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('checkout.checkout'))
    
    # Form validation failed
    cart = get_cart()
    cart_items = []
    total = 0
    
    for product_id, item_data in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            item_total = product.price * item_data['quantity']
            cart_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'total': item_total
            })
            total += item_total
    
    return render_template('checkout/checkout.html', 
                         cart_items=cart_items, 
                         total=total, 
                         form=form,
                         stripe_public_key=current_app.config['STRIPE_PUBLISHABLE_KEY'])

@checkout_bp.route('/success')
@login_required
def success():
    session_id = request.args.get('session_id')
    
    if session_id:
        try:
            # Retrieve the session from Stripe
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            
            if checkout_session.payment_status == 'paid':
                # Update order status
                order = Order.query.filter_by(
                    stripe_payment_intent_id=session_id,
                    user_id=current_user.id
                ).first()
                
                if order:
                    order.status = 'paid'
                    db.session.commit()
                    
                    # Clear cart
                    session.pop('cart', None)
                    
                    # Send confirmation email (optional)
                    # send_order_confirmation_email(order)
                    
                    flash('Payment successful! Your order has been confirmed.', 'success')
                    return render_template('checkout/success.html', order=order)
        
        except stripe.error.StripeError as e:
            flash(f'Error verifying payment: {str(e)}', 'error')
    
    flash('Payment verification failed.', 'error')
    return redirect(url_for('index'))

@checkout_bp.route('/cancel')
@login_required
def cancel():
    flash('Payment was cancelled.', 'info')
    return redirect(url_for('cart.view_cart'))

@checkout_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return 'Invalid signature', 400
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Update order status
        order = Order.query.filter_by(
            stripe_payment_intent_id=session['id']
        ).first()
        
        if order:
            order.status = 'paid'
            db.session.commit()
            
            # Send confirmation email
            # send_order_confirmation_email(order)
    
    return 'Success', 200