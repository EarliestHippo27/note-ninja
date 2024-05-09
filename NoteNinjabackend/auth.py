from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import User
from . import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message, Mail

auth = Blueprint('auth', __name__)

@auth.route('/go', methods=['GET', 'POST'])
def go():
    return render_template("go.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
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
    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    data = request.form
    print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm_password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be more than 3 characters.', category='error')
        elif len(username) < 5:
            flash('Username must be more than 4 characters', category='error')    
        elif password1 != password2:
           flash('Passwords don\'t match.', category='error')    
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
                   
    return render_template("register.html")

def send_mail(user: User):
    token = user.get_token()
    print(token)
    msg = Message('Password Reset Request', sender='noreply@noteninja.com', recipients=[user.email])
    msg.body = f'''To reset your password, please follow the link below:

    {url_for('auth.reset_token', token=token, _external=True)}

    If you didn't send a password reset request, please ignore this message.
    '''

    mail.send(msg)
    pass

@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    data = request.form
    print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            # if no such user
            flash('No account with that Email', category='error')
        else:
            # if user exists
            send_mail(user)
            flash('Reset Password Request Sent, Check your email', category='success')
            return redirect(url_for('auth.login'))

    return render_template("reset_request.html")

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_token(token):
    print(token)
    user = User.verify_token(token)
    if user == None:
        flash('That is an Invalid/Expired Token', category='error')
        return redirect(url_for('auth.reset'))
    #From This point, the token is valid for some user
    if request.method == 'POST':
        password1 = request.form.get('password')
        password2 = request.form.get('confirm_password')
        if password1 != password2:
                flash('Passwords do not match.', 'error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters long.', 'error')
        else:
            hashed_password = generate_password_hash(password1)
            user.password = hashed_password
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('change_password.html', token=token)