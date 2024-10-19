from flask import render_template,session,redirect,url_for,request,flash
from .forms import RegistrationForm
from shop import app, db,bcrypt
import os
from .models import User


@app.route('/')
def home():
    return render_template('admin/index.html', title='Admin Page')


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