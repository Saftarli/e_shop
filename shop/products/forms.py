from flask_wtf.file import FileAllowed,FileField,FileRequired
from wtforms import Form, IntegerField,StringField, BooleanField, TextAreaField, validators


class Addproducts(Form):
    name  = StringField('Name',[validators.DataRequired()])
    price = IntegerField('Price',[validators.DataRequired()])
    discount = IntegerField('Discount',default=0)
    stock = IntegerField('Stock',[validators.DataRequired()])
    discription = TextAreaField('Discount', [validators.DataRequired()])
    colors = TextAreaField('Colors', [validators.DataRequired()])
    

    image_1 = FileField('Image 1',
                        validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only, please')])
    image_2 = FileField('Image 2',
                        validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only, please')])
    image_3 = FileField('Image 3',
                        validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only, please')])