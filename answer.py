import connection as c


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
