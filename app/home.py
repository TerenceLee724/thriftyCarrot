from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime

from .models.productModel import ProductModel
from .models.oldCartModel import OldCartModel
from .models.oldCartContentModel import OldCartContentModel

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask import Blueprint
bp = Blueprint('home', __name__)

class userEntry(FlaskForm):
    uid = StringField('UserID', validators=[DataRequired()])
    submit = SubmitField('Search For Carts')

@bp.route('/home', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        #TODO: new cart button
        #TODO: *expansion* view cart in progress
        #TODO: cart history instead of products/purchase history
        products = ProductModel.get_all(datetime.datetime(2022, 10, 1, 0, 0, 0))
        purchases = OldCartModel.get_all_by_uid_since(
             current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        
        carts = OldCartModel.get_recent_three_by_uid(current_user.id)
        for cart in carts:
            cart.time_created = cart.time_created.strftime("%b %d, %Y")
        cartContent = OldCartContentModel.get_content_of_recent_three_by_uid(current_user.id)

        return render_template('home.html',
                current_user=current_user,
                avail_products=products,
                purchase_history=purchases,
                carts=carts,
                cartContent=cartContent)
    else:
        return redirect(url_for('users.login'))
