from flask import Blueprint, render_template, request, flash, redirect, url_for 
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user 

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
#function to get login info
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #validate status of person logging in
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))   
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

#logout redirects to login page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
#function for getting account set up info
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #logic behind checking various parts of setting up account
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4: 
            flash('Email must be longer than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be longer than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords must match', category='error')
        elif len(password1) < 7: 
            flash('Password must be longer than 6 characters.', category='error')
        else:
            #add user to database if all checks completed
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Successful entry.', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)