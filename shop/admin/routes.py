from flask import render_template,session,redirect,url_for,request,flash
from .forms import RegistrationForm
from shop import app, db

@app.route('/')
def home():
    return "Home page  of your shop"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # user = User(form.username.data, form.email.data,
        #             form.password.data)
        # db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, tiitle="Registeration page")