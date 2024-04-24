from flask_bcrypt import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from .db import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')
@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(f"select * from app_user where email = %s", (email, ))
    user_data = cursor.fetchone()

    if not user_data or not check_password_hash(user_data[3], password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    user = User(*user_data)
    login_user(user, remember=remember)
    
    return redirect(url_for('index'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not email or not name or not password or not confirm_password:
        flash('All fields are required!', 'error')
        return render_template('signup.html')

    if password != confirm_password:
        flash('Passwords do not match!', 'error')
        return render_template('signup.html')

    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(f"select * from app_user where email = %s", (email, )) 
    user = cursor.fetchone()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    
    hashed_password = generate_password_hash(password)
    cursor.execute(f"insert into app_user (email, username, password_hash) values (%s, %s, %s)", (email, name, hashed_password))

    conn.commit()
    cursor.close()
    conn.close()
    
    

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.initial'))