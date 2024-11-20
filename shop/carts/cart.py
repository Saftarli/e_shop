from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from shop.products.models import Addproduct,Brand,Category

def MagerDicts(dict1, dict2):
    # Merge dictionaries, adding quantities if items exist
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        for key in dict2:
            if key in dict1:
                dict1[key]["quantity"] = str(int(dict1[key]["quantity"]) + int(dict2[key]["quantity"]))
            else:
                dict1[key] = dict2[key]
        return dict1
    return False

@app.route('/addcart', methods=["POST"])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        color = request.form.get('colors')  # Seçilən rəngi alın
        product = Addproduct.query.filter_by(id=product_id).first()
        
        
        
        if not product:
            flash("Product not found", "danger")
            return redirect(request.referrer)

        if product_id and quantity and color and request.method == "POST":
            DictItems = {
                product_id: {
                    "name": product.name,
                    "price": product.price,
                    "discount": product.discount,
                    "color": color,  # Burada seçilmiş rəngi əlavə edin
                    "quantity": quantity,
                    "image": product.image_1, 
                    "colors": product.colors
                }
            }

            if 'Shoppingcart' in session:
                session["Shoppingcart"] = MagerDicts(session["Shoppingcart"], DictItems)
            else:
                session["Shoppingcart"] = DictItems
            
            session.modified = True  # Sessiya dəyişikliklərini qeyd edin
            flash("Product added to cart", "success")
        return redirect(request.referrer)

    except Exception as e:
        print(f"Error the adding to cart: {e}")
        flash("An error occurred while adding to cart", "danger")
        return redirect(request.referrer)




@app.route('/carts')
def getCart():
    brands = Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount =(product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%.2f" % (.06 * float(subtotal)))
        grandtotal += float("%.2f" %(1.06 * subtotal))
        
    return render_template('products/carts.html', tax=tax, grandtotal=grandtotal, brands=brands, categories=categories)

@app.route('/updatecart<int:code>', methods=['POST'])
def updateCart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
    
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key,None)
                flash('Item is deleted')
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/clearcart')
def clearcart():
    try:
        
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)   
    
    
    
@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

