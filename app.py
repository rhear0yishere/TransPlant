import os
from flask import Flask, request, g, render_template, flash, redirect, url_for

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

from flask_cors import CORS

import models
from models import Review, userPlants, User

from forms import ReviewForm, SignUpForm, LoginForm, PlantForm, EditReviewForm, EditProfileForm


app = Flask(__name__, static_url_path='/static')
CORS(app)

DEBUG = True
PORT = 8000

app.secret_key = 'adkjfalj.adflja.dfnasdf.asd'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def landingPage():
    return render_template('landing.html')


@app.route('/swipe', methods=['GET', 'POST'])
def swipePage(swipe=None):
    form3 = PlantForm()
    form4 = EditProfileForm()

    if form3.validate_on_submit():
        models.userPlants.create(user=g.user._get_current_object(),
                                 userPlants=form3.userPlants.data)

    return render_template('swipe.html', swipe=swipe, form3=form3, form4=form4)


@app.route('/profile', methods=['GET', 'POST'])
def stream(username=None):
    form = ReviewForm()
    form2 = EditReviewForm()
    form4 = EditProfileForm()

    formData = form2.idNumber.data

    user = models.User.select().where(
        models.User.username == current_user.username).get()
    stream = user.stream.limit(100)
    stream2 = user.swipe.limit(100)

    if form2.validate_on_submit():
        if form2.idNumber.data == None:
            print("SAAAAAAAAAD")
        else:
            intFormData = int(formData)
            print(intFormData)
            if Review.id == intFormData and 0 < form.rating.data < 6:
                plant = Review.get(Review.id == (intFormData))
                plant.text = form2.text.data
                plant.rating = form2.rating.data
                plant.plant = form2.plant.data
                plant.save()
            else:
                flash(
                    "Could not edit review, please ensure you have filled out all the fields correctly")

    return render_template('stream.html', stream=stream, stream2=stream2, form=form, form2=form2, form4=form4, username=username, user=user)


@app.route('/create', methods=['POST'])
def create_review():
    form = ReviewForm()
    if form.validate_on_submit() and 0 < form.rating.data < 6:
        models.Review.create(user=g.user._get_current_object(),
                             plant=form.plant.data,
                             rating=form.rating.data,
                             text=form.text.data)
        return redirect(url_for('stream'))
    else:
        flash("Could not submit review, please ensure you have filled out all the fields correctly")
        return redirect(url_for('stream'))


@app.route('/editProfile', methods=['POST'])
def edit_profile():
    form4 = EditProfileForm()
    if form4.validate_on_submit():
        print("AYYYYO")
        user = models.User.select().where(
            models.User.username == current_user.username).get()
        user.username = form4.username.data
        user.city = form4.city.data
        user.save()
        return redirect(url_for('stream'))
    else:
        return redirect(url_for('stream'))


@app.route('/delete', methods=['GET'])
def delete():
    reviews = models.Review.select()
    idNumber = request.args.get('idNumber')
    if idNumber == Review.id:
        plant = Review.get(Review.id == idNumber)
        plant.delete_instance()
    return redirect(url_for('stream'))


@app.route('/signup', methods=('GET', 'POST'))
def signupPage():
    form = SignUpForm()
    if form.validate_on_submit():
        flash('signup successful')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            city=form.city.data,
            password=form.password.data
        )
        return redirect(url_for('landingPage'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Not a match")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Logged In!")
                return redirect(url_for('swipePage'))
            else:
                flash("Not a match!")

    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged Out")
    return redirect(url_for('loginPage'))


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='rroy',
            email="rhea@rhea.com",
            password='password',
            city='San Jose',
            admin=True
        )
    except ValueError:
        pass

    app.run(debug=DEBUG, port=PORT)
