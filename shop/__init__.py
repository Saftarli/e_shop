from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shop.db'
app.config['SECRET_KEY']='alahsxlanxlanj12331'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from shop.admin import routes
from shop.products import routes
# if __name__ == "__main__":
#     app.run(debug=os.getenv('FLASK_DEBUG')=='1')
#     # with app.app_context():
#     #     db.create_all()