import csv

QUESTION_FILE = 'data/question.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWERS_FILE = 'data/answer.csv'


def get_all_questions():
    user_stories = []
    with open(QUESTION_FILE) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            user_stories.append(row)
        print(user_stories)
        return user_stories


def get_headers():
    headers = []
    for header in DATA_HEADER:
        headers.append(header.replace('_', ' ').capitalize())
    return headers


def get_all_answers():
    with open(ANSWERS_FILE, 'r') as file:
        f_data = csv.reader(file, quotechar='"')

        f_data_parsed = list(f_data)

    return f_data_parsed


def write_answer(data):
    with open(ANSWERS_FILE, 'r') as file:
        f_data = file.readlines()

    f_data.append(','.join(data) + '\n')

    with open(ANSWERS_FILE, 'w') as file:
        file.writelines(f_data)


def delete_answer(id):
    answers = get_all_answers()
    for answer in answers:
        if id == answer[0]:
            answers.remove(answer)

    answers_with_newlines = list()
    for answer in answers:
        answers_with_newlines.append(','.join(answer) + '\n')

    with open(ANSWERS_FILE, 'w') as file:
        file.writelines(answers_with_newlines)
