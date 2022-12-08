from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
import datetime
from .models.productModel import ProductModel

from flask import Blueprint
bp = Blueprint('products', __name__)

class userEntry(FlaskForm):
    k = StringField('Number of Products', validators=[DataRequired()])
    submit = SubmitField('Search')

# back end endpoint
@bp.route('/products', methods=['GET', 'POST'])
def products():
    form = userEntry()
    if form.validate_on_submit():
        products = ProductModel.getKMostExpensive(form.k.data)
    else:
        products = None
    # render the page by adding information to the oldCarts.html file
    return render_template('products.html',
                            form=form,
                            products=products)


class featureEntry(FlaskForm):
    name = StringField('Product name', validators=[DataRequired()])
    minprice = IntegerField('Minimum price')
    maxprice = IntegerField('Maximum price')
    category = SelectField('Category', coerce=str)
    store = SelectField('Store',coerce=str)
    submit = SubmitField('Search')

@bp.route('/browse-products', methods=['GET', 'POST'])
def browseproducts():
    featureform = featureEntry()
    allproducts = ProductModel.get_all()
    categorychoices = []
    storechoices= []
    for i in allproducts:
        if i.category not in categorychoices:
            categorychoices.append(i.category)
        if i.store not in storechoices:
            storechoices.append(i.store)
    featureform.category.choices = categorychoices
    featureform.store.choices = storechoices
    if featureform.validate_on_submit():
        products = ProductModel.get_by_feature(featureform.name.data, featureform.minprice.data, featureform.maxprice.data,featureform.category.data, featureform.store.data)
    else:
        products = None
    
    # render the page by adding information to the oldCarts.html file
    return render_template('browse-products.html',
                            featureform=featureform,
                            products=products,
                            allproducts=allproducts)