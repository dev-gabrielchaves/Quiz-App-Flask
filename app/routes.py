from flask import render_template, redirect, url_for, flash, session
from app import app, bcrypt, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

@app.route('/')
def home():
    return render_template('home.html', title='Home', username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('id'):
        return redirect(url_for('home'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                flash("You've been logged in successfully!")
                session['id'] = user.id
                session['email'] = user.email
                session['username'] = user.username
                return redirect(url_for('home'))
            else:
                flash("Couldn't find the user. Please check your email and password.")
        return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('id'):
        return redirect(url_for('home'))
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, 
                        email=form.email.data,
                        password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("You've been registered successfully!")
            session['id'] = user.id
            session['email'] = user.email
            session['username'] = user.username
            return redirect(url_for('home'))
        return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))