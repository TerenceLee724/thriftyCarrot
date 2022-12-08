from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
import datetime
import random
random.seed(0)

from .models.productModel import ProductModel
from .models.oldCartModel import OldCartModel
from .models.oldCartContentModel import OldCartContentModel
from .models.preferenceModel import PreferenceModel


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired

from flask import Blueprint
bp = Blueprint('home', __name__)

class userEntry(FlaskForm):
    uid = StringField('UserID', validators=[DataRequired()])
    submit = SubmitField('Search For Carts')

class reviewEntry(FlaskForm):
    like_dislike = BooleanField('Give a fresh carrot?')
    submit = SubmitField('AddReview')

@bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    #TODO: *expansion* view cart in progress
    products = ProductModel.get_all(datetime.datetime(2022, 10, 1, 0, 0, 0))
    purchases = OldCartModel.get_all_by_uid_since(
        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    
    carts = OldCartModel.get_recent_three_by_uid(current_user.id)
    for cart in carts:
        cart.time_created = cart.time_created.strftime("%b %d, %Y")
    cartContent = OldCartContentModel.get_content_of_recent_three_by_uid(current_user.id)
    purchase_category = OldCartContentModel.get_count_by_category(current_user.id)
    last_cart_prices = OldCartContentModel.get_last_cart_prices(current_user.id)
    data = []
    data_length = 0 
    last_cart = []
    last_cart_length = 0
    for product in last_cart_prices:
        if last_cart_length == 0:
            last_cart.append(["Product name","Total price"])
        last_cart_length+=1
        last_cart.append([product.product_name, float(product.price)])
    for purchase in purchase_category:
        if data_length == 0:
            data.append(["Category","Count"])
        data_length+=1
        data.append([purchase.category,purchase.pid])
    for content in cartContent:
        content.review = PreferenceModel.get_product_review(current_user.id, content.pid)
        if(content.review): content.like_dislike = content.review[0].like_dislike
    count = data_length
    return render_template('home.html',
            current_user=current_user,
            avail_products=products,
            purchase_history=purchases,
            category_data = data,
            last_cart = last_cart,
            count = count,
            carts=carts,
            cartContent=cartContent)

