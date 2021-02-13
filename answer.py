import connection as c

def get_question_data(question_id):

    questions = c.get_questions()
    que_dict = dict()
    headers = questions[0]
    for iterator in range(1, len(questions)):
        if question_id == questions[iterator][0]:
            this_question = questions[iterator]
    if this_question in locals():
        for counter, header in enumerate(headers):
            que_dict[header] = this_question[counter]

    return que_dict