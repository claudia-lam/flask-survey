from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def display_survey_start():
    """display root page with title, instructions, and start survey button"""

    return render_template('survey_start.html', current_survey=survey)

@app.post('/begin')
def redirect_to_question():
    """redirect /begin to first question"""

    session["responses"] = []

    return redirect("/questions/0")

@app.get('/questions/<int:id>')
def questions_survey(id):
    """display survey question with answer options"""

    if len(session["responses"]) == len(survey.questions):
        return redirect('/completion')

    if id != len(session["responses"]):
        return redirect(f'/questions/{len(session["responses"])}')

    return render_template('question.html',
                           question=survey.questions[id])

@app.post('/answer')
def handle_answer():
    """save answers and redirects page to next question or completion page"""

   #get the response choice
    answer = request.form['answer']

   #add response to session
    survey_responses = session["responses"]
    survey_responses.append(answer)
    session["responses"] = survey_responses

    if len(survey_responses) != len(survey.questions):
        return redirect(f"/questions/{len(survey_responses)}")
    else:
        return redirect('/completion')

@app.get('/completion')
def complete_survey():
    """display questions and responses"""
    survey_responses = session["responses"]

    return render_template('completion.html', questions=survey.questions,
                            responses=survey_responses)



