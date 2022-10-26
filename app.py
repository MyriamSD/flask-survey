from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# responses = []
RESPONSES_KEY = "responses"




@app.route('/')
def home():
    instructions = satisfaction_survey.instructions
    title = satisfaction_survey.title
    return render_template("root.html", instructions=instructions, title=title)


@app.route('/start' , methods=["POST"])
def start():
    # num = satisfaction_survey.questions[id]
    # session.clear()
    # session[responses] = []
    session[RESPONSES_KEY] = []
    
    return redirect("/questions/0")



@app.route('/questions/<int:numb>')
def ask_questions(numb):
    # responses = session.get(responses)
    question = satisfaction_survey.questions[numb]
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != numb):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {numb}.")
        return redirect(f"/questions/{len(responses)}")

    if ()
    
    return render_template("questions.html", question=question, question_num=numb)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/end")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/end")
def end():
    """Survey complete. Show completion page."""

    return render_template("end.html")