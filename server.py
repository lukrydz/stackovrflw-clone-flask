from flask import Flask, render_template, url_for, redirect, request
import connection as c

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route("/", methods=['GET', 'POST'])
@app.route('/questions', methods=['GET', 'POST'])
def vote_on_answer():
    questions = c.get_questions()
    counter = c.open_counter_file()
    if request.method == 'POST':
        form = request.form
        vote = form['vote']
        if vote == "vote_up":
            counter += 1
        elif vote == "vote_down":
            counter -= 1
    c.save_counter(int(counter))
    return render_template('questions.html', questions=questions, counter=counter)


@app.route('/question')
def question():
    return render_template('question.html')


if __name__ == "__main__":
    app.run(debug=False)
