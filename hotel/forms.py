from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, DateTimeField, IntegerField, \
    TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from hotel.models import admins, rooms
import datetime


class BookRoom(FlaskForm):
    category = SelectField('Room Category', choices=[(i.category, i.category) for i in rooms.query.all()])

    quantity = IntegerField('No. of Rooms', validators=[DataRequired()])

    checkin = DateField('CheckIn', default=datetime.date.today)

    checkout = DateField('CheckOut', default=datetime.date.today)

    name = StringField('Full Name', validators=[DataRequired(), Length(max=50)])

    mobno = StringField('Mobile Number', validators=[DataRequired(), Length(min=0, max=10)])

    submit = SubmitField('Book Now')

    submit2 = SubmitField('Update Booking')

    email = StringField('E-mail', validators=[DataRequired(), Length(max=50)])


class AdminForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Login')

    def validate_username(self, username):
        admin = admins.query.filter_by(username=username.data).first()
        if admin:
            raise ValidationError('This username is already taken. Please choose a different one!')


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=30)])

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    username2 = StringField('New Username', validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password', validators=[DataRequired()])

    password2 = PasswordField('New Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    confirm_password2 = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password2')])

    submit = SubmitField('Sign Up')

    submit2 = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')


class NewRoom(FlaskForm):
    category = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=20)])

    quantity = IntegerField('No. of Rooms', validators=[DataRequired()])

    beds = IntegerField('No. of Beds', validators=[DataRequired()])

    facilities = TextAreaField('Facilities', validators=[DataRequired()])

    price = IntegerField('Price per night', validators=[DataRequired()])

    image = FileField('image', validators=[DataRequired()])

    submit = SubmitField('Add RoomType')

    submit2 = SubmitField('Update')


class delete(FlaskForm):
    submit = SubmitField('Delete')
    submit2 = SubmitField('Edit')
