from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)

bf = Bcrypt()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        passw = request.form.get('passw')
        user = User.query.filter_by(email=email).first()
        if user:
            if bf.check_password_hash(user.passw, passw):
                flash('Login successful', category='success')
                login_user(user)
                return redirect(url_for('view.dashboard'))
            else:
                flash('Username or Password do not match', category='error')
            return redirect(url_for('auth.login'))
        else:
            flash('Login not possible', category='error')
            return redirect(url_for('auth.signup'))
        return redirect(url_for('auth.login'))
    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        name = fname + ' ' + lname
        email = request.form.get('email')
        passw = request.form.get('passw')
        passwc = request.form.get('passwc')
        if passw != passwc:
            flash('Passwords do not match', category='error')
            return redirect(url_for('auth.signup'))
        else:
            new_user = User(name=name, email=email, passw=bf.generate_password_hash(passw))
            db.session.add(new_user)
            db.session.commit()
            flash('Registration Successful!', category='success')
            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.login'))
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out!', category='success')
    return redirect(url_for('auth.login'))