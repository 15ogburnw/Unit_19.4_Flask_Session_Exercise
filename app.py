from crypt import methods
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh-so-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def survey_intro():
    return render_template('intro.html', survey=surveys['satisfaction'])


@app.route('/begin-survey', methods=['POST'])
def init_survey():

    session['responses'] = []

    return redirect('/questions/0')


@app.route('/questions/<int:question_no>')
def show_question(question_no):

    responses = session.get('responses', [])

    if question_no == len(responses):
        return render_template('question.html', question=surveys['satisfaction'].questions[question_no])

    elif len(responses) >= len(surveys['satisfaction'].questions):
        flash('You have already answered all of the survey questions!')
        return redirect('/thanks')

    else:
        flash(
            'You have attempted to access an invalid question! Please continue the survey')
        return redirect(f'/questions/{len(responses)}')


@app.route('/answer', methods=['POST'])
def submit_answer():

    responses = session.get('responses', [])
    answer = request.form["answer"]

    responses.append(answer)
    session['responses'] = responses

    if len(responses) < len(surveys['satisfaction'].questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        return redirect('/thanks')


@app.route('/thanks')
def thank_user():

    return render_template('thanks.html')
