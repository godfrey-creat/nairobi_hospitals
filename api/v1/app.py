#!/usr/bin/python3
'''Contains a Flask web application API.'''

import os
from flask import Flask, jsonify
from flask_cors import CORS

# from api.v1.views import app_views
from flask import Flask,render_template,redirect,url_for,request
from forms.form import LoginForm, HospitalRegistrationForm,UserRegistrationForm
from models.models import User, Hospital,db
from flask_bcrypt import bcrypt
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import login_user, current_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Clean_env_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clean_env1.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Initialising SQLAlchemy with Flask App
db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Try loading the user from both User and Company models
    user = User.query.get(int(user_id))
    if user is None:
        user = Hospital.query.get(int(user_id))
    return user

""" Creating Database with App Context"""
def create_db():
    with app.app_context():
        db.create_all()


@app.errorhandler(404)
def error_404(error):
    '''Handles the 404 HTTP error code.'''
    return jsonify(error="Not found"), 404

@app.errorhandler(400)
def error_400(error):
    '''Handles the 400 HTTP error code'''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error= msg), 400

@app.route('/')
def index():
    """Print Web"""
    return render_template('landing_page/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        login_as = form.login_as.data
        password = form.password.data
        hospitals = Hospital.query.all()
        if login_as == 'hospital':
            hospital = Hospital.query.filter_by(email=email).first()
            if not hospital:
                return render_template('forms/login.html', form=form,msg='The email entered is not associate to any company')
            if hospital and bcrypt.check_password_hash(company.password, password):
                # Authentication successful, redirect to dashboard or company-specific route
                return render_template('home.html',hospitals=hospitals)
            else:
                return render_template('forms/login.html', form=form,msg='Invalid credentials')
        elif login_as == 'user':
            user = User.query.filter_by(email=email).first()
            if not user:
                return render_template('forms/login.html', form=form,msg='Invalid credentials')
            if user and bcrypt.check_password_hash(user.password, password):
                # Authentication successful, redirect to dashboard or client-specific route
                return render_template('home.html',hospitals=hospitals,test='peter')
            else:
                return render_template('forms/login.html', form=form,msg='Invalid credentials')
    return render_template('forms/login.html', form=form)

@app.route('/Hospital_registration', methods=['GET', 'POST'])
def Hospital_registration():
    form = HospitalRegistrationForm()
    print('form avaailable')
    if request.method == 'POST':
        hospitalname = form.hospitalname.data
        service_type = form.service_type.data
        location = form.location.data
        email = form.email.data
        phone_no = form.phone_no.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        hospitals= Hospital.query.filter_by(email=email).first()
        if hospitals:
            return render_template('forms/hospital_reg.html', form=form, msg='Hospital already registered')
        if password != confirm_password:
            return render_template('forms/hospital_reg.html', form=form, msg='Password does not match')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_hospital = Hospital(
            hospitalname=hospitalname,
            service_type=service_type,
            location=location,
            email=email,
            phone_no=phone_no,
            password=hashed_password
        )

        db.session.add(new_hospital)
        db.session.commit()

        return redirect(url_for('login_route'))

    return render_template('forms/hospital_reg.html', form=form)

@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    form = UserRegistrationForm()
    print('form avaailble')
    if request.method == 'POST':
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        confirm_password=form.confirm_password.data
        users= User.query.filter_by(email=email).first()
        if users:
            return render_template('forms/user_reg.html', form=form, msg='Email already exist')
        if password != confirm_password:
            return render_template('forms/user_reg.html', form=form, msg='Password does not match')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login_route',msg='Registration successful, continue to log in'))

    return render_template('forms/user_reg.html', form=form)


@app.route('/booking', methods=['GET', 'POST'])
# @login_required
def booking():
    hospitals= Hospital.query.all()
    return render_template('home.html',hospitals=hospitals)
# if __name__ == '__main__':
#     db.create_all()
