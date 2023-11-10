from flask import render_template, redirect, url_for, flash, session, request
import requests
from app import app, bcrypt, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

@app.route('/')
def home():
    return render_template('home.html', title='Home', username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        flash('You are already logged in!')
        return redirect(url_for('home'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                flash("You've been logged in successfully!")
                session['username'] = user.username
                return redirect(url_for('home'))
            else:
                flash("Couldn't find the user. Please check your email and password.")
        return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'):
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
            session['username'] = user.username
            return redirect(url_for('home'))
        return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Function responsible for generating Quiz questions
def generate_quiz():
    # Getting questions from the TRIVIA API
    response = requests.get('https://opentdb.com/api.php?amount=10&category=9&difficulty=medium&type=multiple')
    if response.status_code == 200:
        # Transforming response into a dictionary and getting the results, that are the questions
        response_dict = response.json()
        results = response_dict['results']
        questions = []
        # The reason of this for loop is just to get the needed information from the results
        for result in results:
            question = {}
            question['question'] = result.get('question')
            question['options'] = result.get('incorrect_answers')
            question['options'].append(result.get('correct_answer'))
            randomize_questions = set(question['options'])
            list_of_randomized_questions = list(randomize_questions)
            question['options'] = list_of_randomized_questions
            question['correct_answer'] = result.get('correct_answer')
            questions.append(question)
        return questions

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if session.get('username'):
        if request.method == 'POST':
            score = 0
            for i, question in enumerate(session['quiz']):
                correct_answer = question.get('correct_answer')
                option_choosen = request.form.get(f'question-{i}')
                if option_choosen == correct_answer:
                    score += 1
            flash(f"You've made {score} question(s) out of 10!")
            return redirect(url_for('home'))
        # Generates a different Quiz each time is called
        elif request.method == 'GET':
            # Saving the Quiz in the session to be used within the 'POST' request
            session['quiz'] = generate_quiz() 
            return render_template('quiz.html', questions=session['quiz'])
    flash('Before starting the Quiz, make sure to login or to subscribe!')
    return redirect(url_for('login'))