from flask import Flask, render_template, url_for, redirect, request, session, flash
import os
import data_handler
from werkzeug.utils import secure_filename
import util

app = Flask(__name__)

app.secret_key = b'\x90\xb5\x14\x04k\x99\x92O\xce1n\xd8K\x83Cd'

UPLOAD_FOLDER = './static/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
@app.route('/index')
def index():

    try:
        logged_user, username = data_handler.verify_session(session['session_id'])
    except:
        logged_user, username = None, None

    return render_template('index.html', userid=logged_user, username=username)


@app.route("/registration", methods=['GET'])
def register():
    return render_template('register.html')


@app.route("/registration", methods=['POST'])
def adduser():

    username, password = request.form['username'], request.form['password']

    data_handler.adduser(username, password)

    return redirect(url_for('index'))


@app.route("/login", methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def login_post():

    login, password = request.form['username'], request.form['password']

    if data_handler.check_credentials(login, password):
        session['session_id'] = data_handler.open_session(login)
    else:
        flash('Invalid credentials.')
        return redirect(url_for('login_get'))

    return redirect(url_for('index'))


@app.route('/new-answer', methods=['GET', 'POST'])
def add_question():

    logged_user, username = data_handler.verify_session(session['session_id'])

    if not logged_user:
        return redirect(url_for('login_get'))

    if request.method == 'POST':
        title = request.form['title']
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

        data_handler.post_question(logged_user, title, message, image)
        question_data = data_handler.get_latest_question()
        print(question_data)
        return redirect(url_for(
            'question',
            question_id=question_data['id']))

    return render_template('add_question.html', userid=logged_user, username=username)


@app.route('/question/<question_id>/edit', methods=['GET'])
def display_edit_question(question_id):
    logged_user, username = data_handler.verify_session(session['session_id'])

    if not logged_user:
        return redirect(url_for('login_get'))

    question_data = data_handler.get_question_by_id(question_id)
    return render_template('edit_question.html',
                           question_id=question_id,
                           title=question_data['title'],
                           message=question_data['message'],
                           userid=logged_user,
                           username=username)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):

    question_data = data_handler.get_question_by_id(question_id)

    image = ''

    if 'image' in request.files:

        file = request.files['image']
        if file and util.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            image = path

    new_title = request.form['title']
    new_message = request.form['message']

    data_handler.question_update(question_id, new_title, new_message, image)

    return redirect(url_for('question', question_id=question_id))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    # TODO delete tags for question ID

    logged_user, username = data_handler.verify_session(session['session_id'])
    if not logged_user:
        return redirect(url_for('login_get'))

    if data_handler.get_question_by_id(id=question_id)['author'] != logged_user:
        flash('You are not the owner')
        return redirect(url_for('index'))

    answers = data_handler.get_answers_for_question(question_id)

    for answer_to_delete in answers:
        comments_for_answers = data_handler.fetch_comments(
            answer_to_delete['id'],
            'answer')
        for comment_to_delete in comments_for_answers:
            data_handler.delete_comment(comment_to_delete['id'])

        data_handler.delete_answer(answer_to_delete['id'])

    comments_for_question = data_handler.fetch_comments(question_id, 'question')
    for comment_to_delete in comments_for_question:
        data_handler.delete_comment(comment_to_delete['id'])

    data_handler.delete_question(question_id)

    return redirect(url_for('questions'))


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    logged_user, username = data_handler.verify_session(session['session_id'])
    questions_list = data_handler.get_all_questions()

    return render_template('questions.html',
                           questions_list=questions_list, userid=logged_user, username=username)


@app.route('/question/<question_id>')
def question(question_id):
    logged_user, username = data_handler.verify_session(session['session_id'])

    if question_id == '':
        return redirect('questions')

    question_data = data_handler.get_question_by_id(id=question_id)
    answers = data_handler.get_answers_for_question(question_id=question_id)
    comments = data_handler.fetch_comments(id=question_id, mode='question')

    comment_for_answers = dict()

    for answer in answers:
        comment_for_answers[answer['id']] = data_handler.fetch_comments(id=answer['id'],
                                                                        mode='answer')

    return render_template('question.html',
                           question_data=question_data,
                           answers=answers,
                           comments_for_question=comments,
                           comment_for_answers=comment_for_answers,
                           userid=logged_user, username=username)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    logged_user, username = data_handler.verify_session(session['session_id'])

    if not logged_user:
        return redirect(url_for('login_get'))

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

        data_handler.post_answer(logged_user, question_id, message, image)

        return redirect(url_for('question', question_id=question_id))

    question_data = data_handler.get_question_by_id(id=question_id)

    return render_template('add_answer.html', question_dictionary=question_data, userid=logged_user, username=username)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    """
    TODO: delete image when uploading new one.
    """
    logged_user, username = data_handler.verify_session(session['session_id'])

    if not logged_user:
        return redirect(url_for('login_get'))

    answer_data = data_handler.get_answer_by_id(answer_id)
    question_data = data_handler.get_question_by_id(id=answer_data['question_id'])

    referrer_question = answer_data['question_id']

    # if there is POST form make an update
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

    # else show form with answer data
    return render_template('edit_answer.html',
                           answer_data=answer_data,
                           question_dictionary=question_data,
                           userid=logged_user, username=username)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    """TODO: delete belonging comments for answer"""

    logged_user, username = data_handler.verify_session(session['session_id'])

    if not logged_user:
        return redirect(url_for('login_get'))


    referrer_question = data_handler.get_answer_by_id(answer_id)['question_id']

    if data_handler.get_answer_by_id(answer_id)['author'] != logged_user:
        flash('You are not an owner!')
        return redirect(url_for('question', question_id=referrer_question))

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
    logged_user, username = data_handler.verify_session(session['session_id'])

    question_data = data_handler.get_question_by_id(question_id)

    if request.method == 'POST':

        message = request.form['message']

        data_handler.post_comment(logged_user, message, 'question', question_id)

        return redirect(url_for('question', question_id=question_id))

    else:

        return render_template('add_comment.html', question_data=question_data)


@app.route('/answer/<question_id>/<answer_id>/new-comment', methods=['GET', 'POST'])
def comment_answer(question_id, answer_id):
    logged_user, username = data_handler.verify_session(session['session_id'])

    answer_data = data_handler.get_answer_by_id(answer_id)
    referrer_question = answer_data['question_id']

    if request.method == 'POST':

        message = request.form['message']

        data_handler.post_comment(logged_user, message, 'answer', question_id, answer_id)

        return redirect(url_for('question', question_id=referrer_question))

    else:

        return render_template('comment_answer.html', answer_data=answer_data)


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment_data = data_handler.get_comment_by_id(comment_id)
    print(comment_data)
    referrer_question = comment_data['question_id']

    if request.method == 'POST':
        message = request.form['message']

        data_handler.edit_comment(comment_id=comment_id, message=message)

        return redirect(url_for('question', question_id=referrer_question))

    return render_template('edit_comment.html', comment_data=comment_data)


@app.route('/comments/<comment_id>/delete', methods=['GET'])
def delete_comment(comment_id):
    data_handler.delete_comment(comment_id=comment_id)

    return redirect(request.referrer)


@app.route('/user/<user_id>', methods=['GET'])
def userpage(user_id):
    logged_user, username = data_handler.verify_session(session['session_id'])

    # User id, User name (link to user page if implemented), Registration date

    user_data = data_handler.get_user_data_by_id(user_id=user_id)

    user_questions = data_handler.get_questions_by_author(user_id)
    user_answers = data_handler.get_answers_by_author(user_id)
    user_comments = data_handler.get_comments_by_author(user_id)

    # Count of asked questions (if binding implemented)
    # Count of answers (if binding implemented)
    # Count of comments (if binding implemented)
    # Reputation (if implemented)

    return render_template('userpage.html', userid=logged_user, username=username, user_data=user_data,
                           user_questions=user_questions, user_answers=user_answers, user_comments=user_comments)

@app.route('/users')
def users():

    return ""


if __name__ == "__main__":
    app.run(debug=True)
