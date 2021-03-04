from flask import Flask, render_template, url_for, redirect, request
import os
import data_handler
import logging
from werkzeug.utils import secure_filename
import util

QUESTION_ID_INDEX = 0
QUESTION_TIME_INDEX = 1
QUESTION_VIEW_INDEX = 2
QUESTION_VOTE_INDEX = 3
QUESTION_TITLE_INDEX = 4
QUESTION_MESSAGE_INDEX = 5
QUESTION_IMAGE_INDEX = 6

app = Flask(__name__)

UPLOAD_FOLDER = './static/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=['GET', 'POST'])
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    questions_list = data_handler.get_all_questions()

    # counter = c.open_counter_file()
    # if request.method == 'POST':
    #     vote = request.form['vote']
    #     if vote == "vote_up":
    #         counter += 1
    #     elif vote == "vote_down":
    #         counter -= 1
    # c.save_counter(int(counter))

    print(questions_list)

    # questions are passed, need to update display format

    return render_template('questions.html',
                           questions_list=questions_list,
                           counter=0,
                           QUESTION_ID_INDEX=QUESTION_ID_INDEX,
                           QUESTION_TITLE_INDEX=QUESTION_TITLE_INDEX)


@app.route('/question/<question_id>')
def question(question_id):
    if question_id == '':
        return redirect('questions')

    question_data = data_handler.get_question_by_id(id=question_id)
    answers = data_handler.get_answers_for_question(question_id=question_id)
    comments = data_handler.fetch_comments(id=question_id, mode='question')

    comment_for_answers = dict()

    for answer in answers:
        comment_for_answers[answer['id']] = data_handler.fetch_comments(id=answer['id'], mode='answer')

    return render_template('question.html',
                           question_data=question_data,
                           answers=answers, comments_for_question=comments, comment_for_answers=comment_for_answers)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'POST':

        message = request.form['message']

        image = ''

        if 'image' in request.files:
            print('FOUND FILE')

            file = request.files['image']
            if file and util.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)

                image = path

        data_handler.post_answer(question_id, message, image)

        return redirect(url_for('question', question_id=question_id))

    question_data = data_handler.get_question_by_id(id=question_id)

    return render_template('add_answer.html', question_dictionary=question_data)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    """
    TODO: delete image when uploading new one.
    """

    answer_data = data_handler.get_answer_by_id(answer_id)
    question_data = data_handler.get_question_by_id(id=answer_data['question_id'])

    referrer_question = answer_data['question_id']

    # IF THERE IS POST FORM MAKE UPDATE
    if request.method == 'POST':

        image = ''

        if 'image' in request.files:

            file = request.files['image']
            if file and util.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)

                image = path

        new_message = request.form['message']

        data_handler.answer_update(answer_id, new_message, image)

        return redirect(url_for('question', question_id=referrer_question))

    # ELSE SHOW FORM WITH ANSWER DATA
    return render_template('edit_answer.html', answer_data=answer_data, question_dictionary=question_data)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):

    referrer_question = data_handler.get_answer_by_id(answer_id)['question_id']

    data_handler.delete_answer(answer_id)

    return redirect(url_for('question', question_id=referrer_question))


@app.route('/answer/<answer_id>/<vote_up_or_down>')
def vote(answer_id, vote_up_or_down):
    referrer_question = data_handler.get_answer_by_id(answer_id)['question_id']

    value = 1 if vote_up_or_down == 'vote_up' else -1

    print(answer_id, value)

    data_handler.vote_answer(answer_id=answer_id, value=value)
    return redirect(url_for('question', question_id=referrer_question))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def comment_question(question_id):

    question_data = data_handler.get_question_by_id(question_id)

    if request.method == 'POST':

        message = request.form['message']

        data_handler.post_comment(message, question_id, 'question')

        return redirect(url_for('question', question_id=question_id))

    else:

        return render_template('add_comment.html', question_data=question_data)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def comment_answer(answer_id):

    answer_data = data_handler.get_answer_by_id(answer_id)
    referrer_question = answer_data['question_id']

    if request.method == 'POST':

        message = request.form['message']

        data_handler.post_comment(message, answer_id, 'answer')

        return redirect(url_for('question', question_id=referrer_question))

    else:

        return render_template('comment_answer.html', answer_data=answer_data)


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):

    comment_data = data_handler.get_comment_by_id(comment_id)
    if comment_data['question_id']:
        referrer_question = comment_data['question_id']
    else:
        referrer_question = data_handler.get_answer_by_id(id=comment_data['answer_id'])['question_id']

    if request.method == 'POST':

        message = request.form['message']

        data_handler.edit_comment(comment_id=comment_id, message=message)

        return redirect(url_for('question', question_id=referrer_question))

    return render_template('edit_comment.html', comment_data=comment_data)


@app.route('/comments/<comment_id>/delete', methods=['GET'])
def delete_comment(comment_id):

    data_handler.delete_comment(comment_id=comment_id)

    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True)
