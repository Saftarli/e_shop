from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from shop.products.models import Addproduct

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
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        if product_id and quantity and colors and request.method == "POST":
            DictItems = {
                product_id: {
                    "name": product.name,
                    "price": product.price,
                    "discount": product.discount,
                    "color": colors,
                    "quantity": quantity,
                    "image": product.image_1
                }
            }
            # print(DictItems, 'Sefterli')

            if 'Shoppingcart' in session:
                session["Shoppingcart"] = MagerDicts(session["Shoppingcart"], DictItems)
            else:
                session["Shoppingcart"] = DictItems
            print(session["Shoppingcart"], 'Tehmasib')
        return redirect(request.referrer)

    except Exception as e:
        print(f"Error adding to cart: {e}")
        return redirect(request.referrer)
