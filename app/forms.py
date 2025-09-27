from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, BooleanField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo, Optional
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', 
                             validators=[DataRequired(), EqualTo('password')])

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=100)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    featured = BooleanField('Featured Product')
    active = BooleanField('Active', default=True)

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description')

class CustomOrderForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Project Description', validators=[DataRequired()])
    design_file = FileField('Design File', 
                           validators=[FileAllowed(['jpg', 'png', 'jpeg', 'pdf', 'ai', 'psd'])])
    notes = TextAreaField('Additional Notes')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired()], widget=TextArea())

class CheckoutForm(FlaskForm):
    # Billing Information
    billing_first_name = StringField('First Name', validators=[DataRequired()])
    billing_last_name = StringField('Last Name', validators=[DataRequired()])
    billing_email = StringField('Email', validators=[DataRequired(), Email()])
    billing_address = StringField('Address', validators=[DataRequired()])
    billing_city = StringField('City', validators=[DataRequired()])
    billing_state = StringField('State', validators=[DataRequired()])
    billing_zip = StringField('ZIP Code', validators=[DataRequired()])
    billing_country = StringField('Country', validators=[DataRequired()])
    
    # Shipping Information
    same_as_billing = BooleanField('Same as billing address')
    shipping_first_name = StringField('First Name')
    shipping_last_name = StringField('Last Name')
    shipping_address = StringField('Address')
    shipping_city = StringField('City')
    shipping_state = StringField('State')
    shipping_zip = StringField('ZIP Code')
    shipping_country = StringField('Country')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, choices=[(0, 'All Categories')])
    min_price = DecimalField('Min Price', validators=[Optional(), NumberRange(min=0)])
    max_price = DecimalField('Max Price', validators=[Optional(), NumberRange(min=0)])

class AdminCustomOrderForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
    estimated_price = DecimalField('Estimated Price', validators=[Optional(), NumberRange(min=0)])
    final_price = DecimalField('Final Price', validators=[Optional(), NumberRange(min=0)])
    admin_notes = TextAreaField('Admin Notes')