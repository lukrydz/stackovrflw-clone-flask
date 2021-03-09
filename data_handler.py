import connection
import util

DATA_HEADER = ['id',
               'submission_time',
               'view_number',
               'vote_number',
               'title',
               'message',
               'image']


def get_headers():
    headers = []
    for header in DATA_HEADER:
        headers.append(header.replace('_', ' ').capitalize())
    return headers


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                        SELECT * FROM question
                       """)
    return cursor.fetchall()


@connection.connection_handler
def get_question_by_id(cursor, id):
    cursor.execute("""
                        SELECT * FROM question
                        WHERE id=%(id)s
                       """, {'id': id})
    return cursor.fetchone()


@connection.connection_handler
def get_all_answers(cursor):
    cursor.execute("""
                        SELECT * FROM answer
                       """)
    return cursor.fetchall()


@connection.connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute("""
                        SELECT * FROM answer
                        WHERE question_id=%(id)s
                       """, {'id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def get_answer_by_id(cursor, id):
    print(f"id1 - {id}")
    cursor.execute("""
                        SELECT * FROM answer
                        WHERE id=%(id)s
                       """, {'id': id})
    print(f"id - {id}")
    return cursor.fetchone()


def post_question(title, message, image=''):
    submission_time = str(util.get_timestamp())
    vote_number = '0'
    view_number = '0'
    title = str(title)
    message = f'"{message}"'
    image = image

    data = {'submission_time': submission_time,
            'view_number': view_number,
            'vote_number': vote_number,
            'title': title,
            'message': message,
            'image': image}

    write_question(data=data)


def post_answer(question_id, message, image=''):
    submission_time = str(util.get_timestamp())
    vote_number = '0'
    question_id = str(question_id)
    message = f'"{message}"'
    image = image

    data = {'submission_time': submission_time,
            'vote_number': vote_number,
            'question_id': question_id,
            'message': message,
            'image': image}

    write_answer(data=data)


@connection.connection_handler
def write_question(cursor, data: dict) -> None:
    # [answer_id, submission_time, vote_number, question_id, message, image]

    query = """
                INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                VALUES (%(submission_time)s,%(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)
                           """

    cursor.execute(query, data)
    print(cursor.lastrowid)
    return True


@connection.connection_handler
def question_update(cursor, question_id, new_title, new_message, newimage):
    query = """
            UPDATE question
            SET title = %(new_title)s, message = %(new_message)s, image= %(newimage)s
            WHERE id = %(question_id)s        
    """

    cursor.execute(query, {'question_id': question_id, 'new_title': new_title, 'new_message': new_message,
                           'newimage': newimage})


@connection.connection_handler
def write_answer(cursor, data: dict) -> bool:
    # [answer_id, submission_time, vote_number, question_id, message, image]

    query = """
                INSERT INTO answer (
                submission_time,
                vote_number,
                question_id,
                message,
                image)
                VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
                           """

    cursor.execute(query, data)

    return True


@connection.connection_handler
def answer_update(cursor, answer_id, newmessage, newimage):
    if newimage != '':
        query = """
                UPDATE answer
                SET message = %(newmessage)s, image= %(newimage)s
                WHERE id = %(answer_id)s        
        """
    else:
        query = """
                UPDATE answer
                SET message = %(newmessage)s
                WHERE id = %(answer_id)s        
        """
    cursor.execute(
        query,
        {'answer_id': answer_id,
         'newmessage': newmessage,
         'newimage': newimage})


@connection.connection_handler
def vote_answer(cursor, answer_id, value):
    query = """
            UPDATE answer
            SET vote_number = vote_number + %(vote)s
            WHERE id = %(answer_id)s
                       """
    cursor.execute(query, {'vote': value, 'answer_id': answer_id})

    return True


@connection.connection_handler
def delete_question(cursor, id: int):
    query = """
            DELETE FROM question
            WHERE id=%(id)s
                       """

    cursor.execute(query, {'id': id})

    return True


@connection.connection_handler
def delete_answer(cursor, id: int) -> bool:
    query = """
            DELETE FROM answer
            WHERE id=%(id)s
                       """

    cursor.execute(query, {'id': id})

    return True


@connection.connection_handler
def fetch_comments(cursor, id, mode):
    if mode == 'question':
        query = """
            SELECT * FROM comment
            WHERE question_id=%(id)s
        """
    else:
        query = """
                    SELECT * FROM comment
                    WHERE answer_id=%(id)s
                """

    cursor.execute(query, {'id': id})
    return cursor.fetchall()


@connection.connection_handler
def post_comment(cursor, message, mode, id_question="null2", id_answer="null2"):
    submission_time = util.get_timestamp()
    if mode == 'question':
        query_for_question = """
            INSERT INTO comment (question_id, message, submission_time)
            VALUES (%(question_id)s, %(message)s, %(submission_time)s)          
    """
        cursor.execute(
            query_for_question,
            {'question_id': id_question,
             'message': message,
             'submission_time': submission_time})
    else:
        query_for_answer = """
                INSERT INTO comment (question_id, answer_id, message, submission_time)
                VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s)          
        """
        cursor.execute(
            query_for_answer,
            {'question_id': id_question,
             'answer_id': id_answer,
             'message': message,
             'submission_time': submission_time})

    return True


@connection.connection_handler
def delete_comment(cursor, comment_id):
    query = """
            DELETE FROM comment
            WHERE id=%(id)s   
    """
    cursor.execute(query, {'id': comment_id})

    return True


@connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    query = """
            SELECT * FROM comment
            WHERE comment.id=%(comment_id)s
    """
    cursor.execute(query, {'comment_id': comment_id})

    return cursor.fetchone()


@connection.connection_handler
def edit_comment(cursor, comment_id, message):
    query = """
            UPDATE comment
            SET message = %(message)s, edited_count=COALESCE(edited_count, 0) + 1
            WHERE id=%(comment_id)s
    """
    cursor.execute(query, {'message': message, 'comment_id': comment_id})

    return True
