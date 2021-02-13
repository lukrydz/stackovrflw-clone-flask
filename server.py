from flask import Flask, render_template, url_for, redirect, request
import connection as c
import answer

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/questions', methods=['GET', 'POST'])
def vote_on_answer():
    questions = c.get_questions()

    print(questions)

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


@app.route('/question/<question_id>/new-answer', methods=['POST'])
def add_question():

    question_data = answer.get_question_data(question_id)





    #     pass

    #first get questions
    #from questions get the one
    #pass it as argument


    return render_template('add_answer.html', question=selected_question)



if __name__ == "__main__":
    app.run(debug=False)
