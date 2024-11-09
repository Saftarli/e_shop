from flask import render_template,session,redirect,url_for,request,flash
from .forms import RegistrationForm,LoginForm
from shop import app, db,bcrypt
from shop.products.models import Addproduct, Brand, Category
import os
from .models import User




@app.route('/category')
def category():
    if 'email' not in session:
        flash(f'Plaese login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title="Category page", categories=categories)

@app.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'Plaese login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title="Brand page", brands=brands)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.name.data} Thanks for registering','success')
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form, title="Registeration page")

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            print(session, '##############')
            flash('You are logged in','success')
            return redirect(request.args.get('next') or url_for('home'))
        else:
            flash('Invalid email or password','danger')
    return render_template('admin/login.html', form=form, title="Login Page")