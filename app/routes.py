from flask import render_template, redirect, url_for, flash, session
import requests
from app import app, bcrypt, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

@app.route('/')
def home():
    return render_template('home.html', title='Home', username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('id'):
        flash('You are already logged in!')
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
        flash('You are already registered!')
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

@app.route('/quiz')
def quiz():
    if session.get('username'):
        response = requests.get('https://opentdb.com/api.php?amount=10&category=9&difficulty=medium&type=multiple')
        if response.status_code == 200:
            response_dict = response.json()
            results = response_dict['results']
            questions = []
            for result in results:
                question = {}
                question['question'] = result.get('question')
                question['options'] = result.get('incorrect_answers')
                question['options'].append(result.get('correct_answer'))
                set_of_options = set(question['options'])
                question['options'] = set_of_options
                question['correct_answer'] = result.get('correct_answer')
                questions.append(question)
            return render_template('quiz.html', questions=questions)
    flash('Before starting the Quiz, make sure to login or to subscribe!')
    return redirect(url_for('login'))