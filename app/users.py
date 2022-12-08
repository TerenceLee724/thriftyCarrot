from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, URL
from flask_datepicker import datepicker

from .models.userModel import UserModel

from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.home')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/userProfile', methods=['GET', 'POST'])
@login_required
def profile():
    userInfo = UserModel.get_all_by_uid(current_user.id)
    return render_template('userProfile.html',userInfo=userInfo, profilePic = UserModel.profilePicUrl)

class UpdateForm(FlaskForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    email = StringField('Email', validators=[Optional(), Email()])
    birthdate = DateField('Birth Date', validators=[Optional()])
    password = PasswordField('Password', validators=[Optional()])
    password2 = PasswordField(
        'Repeat Password', validators=[
                                       EqualTo('password')])
    submit = SubmitField('Update')
    def validate_email(self, email):
        if UserModel.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

@bp.route('/userUpdate', methods=['GET', 'POST'])
@login_required
def update():
    form = UpdateForm()
    userInfo = UserModel.get_all_by_uid(current_user.id)
    id = current_user.id
    if form.validate_on_submit():
        if form.email.data and UserModel.update_email(form.email.data, id):
            flash('You have updated your email.')
        if form.firstname.data and UserModel.update_firstname(form.firstname.data, id):
            flash('You have updated your first name.')
        if form.lastname.data and UserModel.update_lastname(form.lastname.data, id):
            flash('You have updated your last name.')
        if form.birthdate.data and UserModel.update_birthdate(form.birthdate.data, id):
            flash('You have updated your birth date.')
        if form.password.data and UserModel.update_password(form.birthdate.data, id):
            flash('You have updated your password.')
        return redirect(url_for('users.profile'))
    return render_template('userUpdate.html',userInfo=userInfo, profilePic = UserModel.profilePicUrl, form=form)

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if UserModel.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if UserModel.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

class userEntry(FlaskForm):
    uid = StringField('UserID', validators=[DataRequired()])
    submit = SubmitField('Search')

# back end endpoint
@bp.route('/userinquiry', methods=['GET', 'POST'])
def oldcarts():
    form = userEntry()
    if form.validate_on_submit():
        userInfo = UserModel.get_all_by_uid(form.uid.data)
    else:
        userInfo = None
    # render the page by adding information to the userInquiry.html file
    return render_template('userInquiry.html',
                            form=form,
                            userInfo=userInfo)
