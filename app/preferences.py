from flask import render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, URL
from flask_datepicker import datepicker

from .models.preferenceModel import PreferenceModel

from flask import Blueprint
bp = Blueprint('preferences', __name__)

class userEntry(FlaskForm):
    uid = StringField('UserID', validators=[DataRequired()])
    submit = SubmitField('Search For User Freshy Carrots')

# back end endpoint
@bp.route('/preferences', methods=['GET', 'POST'])
def preferences():
    form = userEntry()
    if form.validate_on_submit():
        recentFresh = PreferenceModel.get_5_recent_fresh_by_uid(form.uid.data)
        recentRotten = PreferenceModel.get_5_recent_rotten_by_uid(form.uid.data)
    else:
        recentFresh = None
        recentRotten = None
    # render the page by adding information to the freshyCarrots.html file
    return render_template('preferences.html',
                            form=form,
                            recentFresh=recentFresh,
                            recentRotten=recentRotten)

class reviewEntry(FlaskForm):
    like_dislike = BooleanField('Give a fresh carrot? (Leave unchecked for rotten carrot)')
    submit = SubmitField('AddReview')

@bp.route('/newPreference', methods=['GET', 'POST'])
@login_required
def update():
    form = reviewEntry()
    uid = current_user.id
    pid = request.args.get('pid', None)
    returnUrl = request.args.get('returnUrl', "home")
    if form.validate_on_submit():
        if(form.like_dislike.data == True): l_d = True
        if(form.like_dislike.data == False): l_d = False
        if PreferenceModel.insert(uid, pid, l_d):
            flash('You have updated your preferences.')
        return redirect(returnUrl)
    return render_template('newPreference.html',form=form)