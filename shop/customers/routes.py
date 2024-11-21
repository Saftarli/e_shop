from flask import redirect,render_template,url_for,flash,request, session, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import db,app, photos, search, bcrypt, login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Register, CustomerOrder  
import secrets 
import os
import json

@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, 
                            username = form.username.data, 
                            email =form.email.data, 
                            password=hash_password, 
                            country=form.country.data, 
                            state=form.state.data,
                            city=form.city.data, 
                            contact=form.contact.data, 
                            address=form.address.data, 
                            zipcode=form.zipcode.data)
        db.session.add(register)
        flash('Welcome {} Thank you for registering'.format(form.name.data), 'success')
        db.session.commit()
        print(register.username)
        return redirect(url_for('login'))
    return render_template('customer/register.html', form=form)

@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are logged in','success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('incorrect email and password')
        return redirect(url_for('customerLogin'))
            
    return render_template('customer/login.html', form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/get_order', methods=['POST', 'GET'])
@login_required
def get_order():
    if current_user.is_authenticated:
        # Unikal faktura nömrəsi
        invoice = secrets.token_hex(5)
        
        # Səbət məlumatını yoxlayın
        if not session.get('Shoppingcart'):
            flash("Səbət boşdur. Sifariş yaradıla bilməz.", "warning")
            return redirect(url_for('getCart'))
        
        try:
            # Yeni sifariş yaradın
            order = CustomerOrder(
                invoice=invoice,
                customer_id=current_user.id,
                orders=session['Shoppingcart']  # JSON formatında sifariş məlumatı
            )
            db.session.add(order)
            db.session.commit()

            # Sessiyanı təmizləyin
            session.pop('Shoppingcart', None)
            flash("Sifarişiniz uğurla göndərildi!", "success")
            return redirect(url_for('home'))
        except Exception as e:
            print(f"Error: {e}")
            flash("Sifariş yaradılarkən problem yarandı.", "danger")
            return redirect(url_for('getCart'))




    