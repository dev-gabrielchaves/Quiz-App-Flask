from flask import render_template, redirect, url_for, flash
from app import app, bcrypt, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("You've been registered successfully!")
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)