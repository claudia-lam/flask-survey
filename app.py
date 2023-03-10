from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get('/')
def display_survey_start():
    """display root page with title, instructions, and start survey button"""
    return render_template('survey_start.html',
                           title=survey.title,
                           instructions=survey.instructions
                           )

@app.post('/begin')
def redirect_to_question():
    """redirect /begin to first question"""
    responses.clear()
    return redirect("/questions/0")

@app.get('/questions/<int:id>')
def questions_survey(id):
    """display survey question with answer submissions""" #with answer options

    # id = int(id)
    return render_template('question.html',
                           question=survey.questions[id])

@app.post('/answer')
def handle_answer():
    """save answers and redirects page to next question or completion page"""
    answer = request.form['answer']
    responses.append(answer)

    if len(responses) != len(survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect('/completion')

@app.get('/completion')
def complete_survey():
    """display questions and responses"""
    return render_template('completion.html', questions=survey.questions,
                            responses=responses)



