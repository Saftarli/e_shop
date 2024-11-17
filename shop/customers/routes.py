from flask import redirect,render_template,url_for,flash,request, session, current_app
from shop import db,app, photos, search, bcrypt
from .forms import CustomerRegisterForm
from .models import Register
import secrets 
import os


@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm(request.form)
    if request.method == 'POST':
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