import connection as c
import util
import data_handler


def get_question_data(question_id):
    questions = c.get_questions()
    question_dict = dict()
    headers = questions[0]

    print(headers)
    this_question = None
    for iterator in range(1, len(questions)):
        if question_id == questions[iterator][0]:
            this_question = questions[iterator]

    if this_question:
        for counter, header in enumerate(headers):
            try:
                question_dict[header] = this_question[counter]
            except IndexError:
                question_dict[header] = ''

    return question_dict


def post_answer(question_id, message, image=''):

    answer_id = str(util.generate_uuid())
    submission_time = str(util.get_timestamp())
    vote_number = '0'
    question_id = str(question_id)
    message = f'"{message}"'
    image = image

    data_handler.write_answer([answer_id, submission_time, vote_number, question_id, message, image])

def get_answers(question_id):

    all_answers = data_handler.get_all_answers()

    HEADERS = all_answers[0].strip().split(',')

    QUESTION_ID_INDEX = HEADERS.index('question_id')

    answers_by_id = list()
    for answer in all_answers[1:]:
        answer = answer.split(',')

        if answer[QUESTION_ID_INDEX] == question_id:
            answer_to_append = dict()
            for header in HEADERS:
                answer_to_append[header] = answer[HEADERS.index(header)]
            answers_by_id.append(answer_to_append)

    return answers_by_id
