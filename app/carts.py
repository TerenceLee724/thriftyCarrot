from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, Form
from wtforms.validators import DataRequired

from datetime import datetime

from .models.cartModel import CartModel, CartListModel, CartContentsModel
from .models.productModel import ProductModel
from .models.oldCartContentModel import OldCartContentModel
from .models.oldCartModel import OldCartModel

from flask import Blueprint
bp = Blueprint('carts', __name__)

# dynamic form adapted from: https://www.rmedgar.com/blog/dynamic-fields-flask-wtf/

class newCartProductsForm(Form):
    product = StringField('Product', validators=[DataRequired()])

class newCartForm(FlaskForm):
    cart_name = StringField('Carrot Cart Name', validators=[DataRequired()])
    products = FieldList(FormField(newCartProductsForm), min_entries=1, max_entries=50)
    submit = SubmitField('Next')

@bp.route('/newcart', methods=['GET', 'POST'])
@login_required
def newcart():        
    uid = current_user.id
    # clear previous cart info from database to start new one
    CartModel.clearCart(uid)
    CartListModel.clearCartList(uid)
    CartContentsModel.clearCartContents(uid)

    form = newCartForm()
    template_form = newCartProductsForm(prefix='products-_-')

    if form.validate_on_submit():
        cart_name = form.cart_name.data
        time_started = datetime.now()
        CartModel.startCart(uid, cart_name, time_started)
        # add product names to cart list
        for product in form.products.data:
            # add product to cart list
            CartListModel.addToCartList(uid, product['product'])
            print(product)
        return redirect(url_for('carts.cartInProgress'))

    return render_template('newCart.html',
                            form = form,
                            _template = template_form)

@bp.route('/cartinprogress', methods=['GET', 'POST'])
@login_required
def cartInProgress():
    # get items cart list by id
    uid = current_user.id
    cart = CartModel.get(uid)
    cartList = CartListModel.get(uid)
    searchResults = []
    for item in cartList:
        searchResult = ProductModel.search_by_name(item.product_name)
        searchResults.append(searchResult)
    cartLength = len(cartList)

    if request.method == 'POST':
        pids = request.form.getlist('product_info')
        for pid in pids:
            CartContentsModel.insert(uid, pid)
        if len(pids)>0:
            return redirect(url_for('carts.cartPurchase'))

    return render_template('cartInProgress.html',
                            cartName = cart[0].cart_name,
                            cartLength = cartLength,
                            cartList = cartList,
                            searchResults = searchResults)

@bp.route('/completecart', methods=['GET', 'POST'])
@login_required
def cartPurchase():
    uid = current_user.id
    cart = CartModel.get(uid)[0]
    cartContents = CartContentsModel.get(uid)
    products = []
    for c in cartContents:
        products.append(ProductModel.get(c.pid))
    
    if request.method == 'POST':
        if request.form.get('submit-button')=="Submit":
            pids = request.form.getlist('product_info')
            cid = OldCartModel.insert(uid, cart.cart_name)
            # only add products checked off to database
            for pid in pids:
                p = pid.split('-')[0]
                q = pid.split('-')[1]
                product = ProductModel.get(p)
                OldCartContentModel.insert(cid, p, product.name, product.price, product.category, product.store, q)
            if len(pids)>1:
                return redirect(url_for('home.home'))
    
    print(products)
    print(cartContents)

    return render_template('completeCart.html',
                            cartName = cart.cart_name,
                            cartLength = len(cartContents),
                            cartContents = cartContents,
                            products = products)