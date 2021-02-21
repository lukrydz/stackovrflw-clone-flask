import connection

DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']

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
    cursor.execute("""
                        SELECT * FROM answer
                        WHERE id=%(id)s
                       """, {'id': id})
    return cursor.fetchone()

@connection.connection_handler
def write_answer(cursor, data: list) -> None:
    #[answer_id, submission_time, vote_number, question_id, message, image]

    query = """
                INSERT INTO answer (id, submission_time, vote_number, question_id, message, image)
                VALUES (%(answer_id)s, %(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
                           """
    cursor.execute(query, {'answer_id': data[0], 'submission_time': data[1], 'vote_number': data[2], 'question_id': data[3], 'message': data[4], 'image': data[5]})

    return True


@connection.connection_handler
def vote_answer(cursor, answer_id, value):

    query = """
            UPDATE answer
            SET vote_number = vote_number + %(vote)s
            WHERE id = 1
                       """
    cursor.execute(query, {'vote': value})

    return True




@connection.connection_handler
def delete_answer(cursor, id: int) -> None:

    query = """
            DELETE FROM answer
            WHERE id=%(id)s
                       """

    cursor.execute(query, {'id': id})

    return True
