from flask import Flask, render_template, url_for, redirect
import connection as c

app = Flask(__name__)


@app.route("/")
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/questions')
def handle_questions():
    questions = c.get_questions()
    counter = c.open_counter_file()

    c.save_counter(counter)
    return render_template('questions.html', questions=questions, counter=counter)


@app.route('/question')
def question():
    return render_template('question.html')


if __name__ == "__main__":
    app.run(debug=False)