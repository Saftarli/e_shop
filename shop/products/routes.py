from flask import redirect,render_template,url_for,flash,request, session
from shop import db,app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets


# @app.route('/')
# def home():
#     return " "

@app.route('/addbrand', methods = ['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Plaese login first','danger')
        return redirect(url_for('login'))
    if request.method== "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    
    
    return render_template('products/addbrand.html', brands ='brands')

@app.route('/updatebrand/<int:id>',methods = ['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    updatebrand= Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method=="POST":
        updatebrand.name = brand
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update Brand Page', updatebrand=updatebrand)


@app.route('/addcat', methods = ['GET','POST'])
def addcat():
    if request.method== "POST":
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The Category {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    
    
    return render_template('products/addbrand.html')

@app.route('/updatecat/<int:id>',methods = ['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    updatecat= Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method=="POST":
        updatecat.name = category
        flash(f'Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Update cagtegory Page', updatecat=updatecat)


@app.route('/addproduct',methods=['GET','POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Plaese login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        brand= request.form.get('brand')
        category = request.form.get('category')
        image_1 =photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+ ".")
        image_2 =photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+ ".")
        image_3 =photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+ ".")
        
        addpro = Addproduct(name=name,price=price,stock=stock,discount=discount,colors=colors,desc=desc,brand_id=brand,category_id=category,image_1=image_1, image_2=image_2,image_3=image_3)
        db.session.add(addpro)
        flash(f'The product {name}  has been added database', 'success')
        db.session.commit()
        return redirect(url_for('home'))
    
    
    return render_template('products/addproduct.html', title="Add Product page", brands=brands, categories=categories, form=form)

