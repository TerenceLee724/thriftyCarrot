from flask import render_template
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import datetime

from .models.oldCartModel import OldCartModel
from .models.oldCartContentModel import OldCartContentModel
from .models.preferenceModel import PreferenceModel
from flask import Blueprint
bp = Blueprint('oldcarts', __name__)

class userEntry(FlaskForm):
    uid = StringField('UserID', validators=[DataRequired()])
    submit = SubmitField('Search For Carts')

# back end endpoint
@bp.route('/oldcarts', methods=['GET', 'POST'])
def oldcarts():
    form = userEntry()
    if  form.validate_on_submit():
        carts = OldCartModel.get_recent_three_by_uid(form.uid.data)
        cartContent = OldCartContentModel.get_most_recent_by_uid(form.uid.data)
    else:
        carts = None
        cartContent = None
    # find all old cart purchases:
    if current_user.is_authenticated:
        currentUserCarts = OldCartModel.get_all_by_uid(
            current_user.id)

        currentUserCartContent = OldCartContentModel.get_all_oldcartcontent_by_uid(
            current_user.id)
    else:
        purchases = None
    
    for content in currentUserCartContent:
        content.review = PreferenceModel.get_product_review(current_user.id, content.pid)
        if(content.review): content.like_dislike = content.review[0].like_dislike

    # render the page by adding information to the oldCarts.html file
    return render_template('oldCarts.html',
                            form=form,
                            carts=carts,
                            cartContent=cartContent,
                            currentUserCarts=currentUserCarts,
                            currentUserCartContent=currentUserCartContent)