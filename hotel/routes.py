import os
import secrets
import smtplib
from flask import render_template, url_for, flash, redirect, request, session, abort
from flask_wtf import form, FlaskForm, _compat
from flask_simplelogin import is_logged_in
from hotel import app, db, bcrypt
from hotel.forms import BookRoom, AdminForm, LoginForm, RegistrationForm, NewRoom, delete
from hotel.models import booking, rooms, admins
from flask_login import login_user, current_user, logout_user

p="Qwerty!@#123"


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title=str("HOME"))


@app.route('/availibility', methods=['GET', 'POST'])
def availibility():
    return render_template("availibility.html", title="CHECK AVAILIBILITY")


@app.route('/book', methods=['GET', 'POST'])
def book():
    form = BookRoom()
    if form.validate_on_submit():
        a = rooms.query.filter_by(category=form.category.data).first()

        if (a.available >= form.quantity.data):
            var = form.quantity.data
            for var in range(0, var):
                b = booking(category=form.category.data, checkin=form.checkin.data, checkout=form.checkout.data,
                            name=form.name.data, mobno=form.mobno.data, status='NOT AVAILABLE')
                db.session.add(b)
                db.session.commit()
            b=booking.query.filter_by(mobno=form.mobno.data).first()
            a.available = a.available - form.quantity.data
            a.booked = a.booked + form.quantity.data
            db.session.commit()
            # 465
            Subject = "Booked Confirmed"
            MESSAGE = "Your Room has been Succsesfully booked\n"+"-"*100+"\n"+"| "+"Booking Number: "+str(b.roomno)+"\n| "+"Number of Rooms: "+str(form.quantity.data)+"\n| "+"Name: "+form.name.data+"\n| "+"Phone Number: "+str(form.mobno.data)+"\n| "+"Check IN: "+str(form.checkin.data)+"\n| "+"Check Out: "+str(form.checkout.data)+"\n"+"-"*100+"\n ** Thank you For your Booking We Wish You Having A Great Time! **"
            m = 'from:{}\nto:{}\nsubject:{}\n{}\n'.format("Maldives Hotel", form.email.data, Subject, MESSAGE)
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("hotel.flask@gmail.com", p)
            server.sendmail("no-reply@gmail.com", form.email.data, m)
            server.quit()
            flash("Your Room has been Successfully Booked\nWe have sent you an email", 'success')
        else:
            flash("Not enough rooms available for the selected category!", 'danger')
        return redirect(url_for('rdirect'))
    return render_template("book.html", title="Book Now", form=form)


@app.route('/update_booking/<string:id>', methods=['GET', 'POST'])
def update_booking(id):
    form = BookRoom()
    if request.method == "POST" and form.submit2:
        b = booking.query.filter_by(roomno=id).first()

        b.checkin = form.checkin.data
        b.checkout = form.checkout.data
        b.name = form.name.data
        b.mobno = form.mobno.data

        db.session.commit()
        flash('Your Booking has been Edited Successfully', 'Success')
        return redirect(url_for('bookings'))
    return render_template("book_update.html", title="Edit Booking", form=form)


@app.route('/rdirect')
def rdirect():
    return render_template("redirect.html")


@app.route('/room_types', methods=['GET', 'POST'])
def room_types():
    decode = _compat
    #        open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)
    room = rooms.query.all()
    return render_template("rooms.html", title="ROOM CATEGORIES", room=room, decode=decode)


@app.route('/rooms2', methods=['GET', 'POST'])
def rooms2():
    dele = delete()
    room = rooms.query.all()
    return render_template("rooms2.html", title="ROOM CATEGORIES", room=room, form=dele)


# for deleting
@app.route('/delete_rom/<string:category>', methods=['POST'])
# @is_logged_in
def delete_room(category):
    d = rooms.query.filter_by(category=category).first()
    db.session.delete(d)
    db.session.commit()
    flash("Room Deleted", "Success")
    return redirect(url_for("rooms2"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.submit:
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        ad = admins(username=form.username.data, password=hashed_password, name=form.name.data)
        db.session.add(ad)
        db.session.commit()
        flash('User Added successfully!', "Success")
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)


# Edit Admin
@app.route('/register_update/<string:id>', methods=['GET', 'POST'])
def register_update(id):
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.submit2:
        hashed_password = bcrypt.generate_password_hash(form.password2.data).decode('utf-8')
        update = admins.query.filter_by(id=id).first()
        update.username = form.username2.data
        update.password = hashed_password
        db.session.commit()
        flash('Profile updated successfully!', "Success")
        return redirect(url_for('managers'))
    return render_template("register_update.html", title='Editing', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin"))
    form = LoginForm()
    if form.validate_on_submit():
        ad = admins.query.filter_by(username=form.username.data).first()
        if ad and bcrypt.check_password_hash(ad.password, form.password.data):
            login_user(ad)
            flash('You are already Logged In', 'Success')
            return redirect(url_for('admin'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template("admin.html", title="Admin")


# for deleting admin
@app.route('/delete_admin/<string:id>', methods=['POST'])
# @is_logged_in
def delete_admin(id):
    d = admins.query.filter_by(id=id).first()
    db.session.delete(d)
    db.session.commit()
    flash("Admin Deleted", "Success")
    return redirect(url_for("managers"))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/newroom', methods=['GET', 'POST'])
def newroom():
    form = NewRoom()
    if form.validate_on_submit():
        image = _compat.to_bytes(form.image.name)
        rtype = rooms(category=form.category.data, quantity=form.quantity.data, beds=form.beds.data,
                      available=form.quantity.data, price=form.price.data, facilities=form.facilities.data, image=image)
        db.session.add(rtype)
        db.session.commit()
        flash("Your Room has been Successfully Booked", 'success')
        return redirect(url_for('rdirect'))
    return render_template("room_category.html", title="Add RoomType", form=form)


# Edit room
@app.route('/room_update/<string:category>', methods=['GET', 'POST'])
def room_update(category):
    form = NewRoom()
    if request.method == "POST" and form.submit2:
        edit = rooms.query.filter_by(category=category).first()

        edit.quantity = form.quantity.data
        edit.available = form.quantity.data
        edit.beds = form.beds.data
        edit.price = form.price.data
        edit.facilities = form.facilities.data

        db.session.commit()
        flash("Your Room has been Successfully Edited", 'success')
        return redirect(url_for('rooms2'))
    return render_template("room_update.html", title="Edit RoomType", form=form)


@app.route('/bookings')
def bookings():
    dels = delete()
    booked = booking.query.all()
    return render_template("bookings.html", title="ROOM CATEGORIES", booked=booked, form=dels)


# for deleting booking
@app.route('/delete_booking/<string:id>', methods=['POST'])
# @is_logged_in
def delete_booking(id):
    d = booking.query.filter_by(roomno=id).first()
    db.session.delete(d)
    db.session.commit()
    flash("Booking Deleted", "Success")
    return redirect(url_for("bookings"))


@app.route('/managers', methods=['GET', 'POST'])
def managers():
    mag = delete()  # for the button from forms.py
    manager = admins.query.all()  # for the data from models.py
    return render_template("managers.html", title="Managers", show=manager, form=mag)
