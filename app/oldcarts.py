from flask import render_template
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import datetime

from .models.oldCartModel import OldCartModel
from .models.oldCartContentModel import OldCartContentModel

from flask import Blueprint
bp = Blueprint('oldcarts', __name__)

class userEntry(FlaskForm):
    uid = StringField('UserID', validators=[DataRequired()])
    submit = SubmitField('Search For Carts')

# back end endpoint
@bp.route('/oldcarts', methods=['GET', 'POST'])
def oldcarts():
    form = userEntry()
    if form.validate_on_submit():
        carts = OldCartModel.get_recent_three_by_uid(form.uid.data)
        cartContent = OldCartContentModel.get_most_recent_by_uid(form.uid.data)
    else:
        carts = None
        cartContent = None
    # find all old cart purchases:
    if current_user.is_authenticated:
        purchases = OldCartModel.get_all_by_uid_since(
            current_user.id, datetime.datetime(2018, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the oldCarts.html file
    return render_template('oldCarts.html',
                            form=form,
                            carts=carts,
                            cartContent=cartContent,
                            purchase_history=purchases)