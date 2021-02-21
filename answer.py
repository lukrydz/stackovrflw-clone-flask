import connection as c
import util
import data_handler

# TODO make it an SQL
def post_answer(question_id, message, image=''):
    answer_id = str(util.generate_uuid())
    submission_time = str(util.get_timestamp())
    vote_number = '0'
    question_id = str(question_id)
    message = f'"{message}"'
    image = image

    data_handler.write_answer(data=[answer_id, submission_time, vote_number, question_id, message, image])

# def update_answer(answer_id, header, new_value):
#     all_answers = data_handler.get_all_answers()
#
#     HEADERS = all_answers[0]
#
#     for answer in all_answers[1:]:
#
#         if answer[HEADERS.index('id')] == answer_id:
#             answer[HEADERS.index(header)] = new_value
#             data_handler.delete_answer(answer_id)
#             data_handler.write_answer(answer)
