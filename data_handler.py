import csv

QUESTION_FILE = 'sample_data/question.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWERS_FILE = 'data/answer.csv'


def get_all_questions():
    user_stories = []
    with open(QUESTION_FILE) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            user_stories.append(row)
        return user_stories


def get_headers():
    headers = []
    for header in DATA_HEADER:
        headers.append(header.replace('_', ' ').capitalize())
    return headers

def get_all_answers():
    with open(ANSWERS_FILE, 'r') as file:
        f_data = file.read().split('\n')

    f_data_parsed = list()
    for line in f_data:
        if len(line) > 0:
            f_data_parsed.append(line)

    return f_data_parsed

def write_answer(data):
    with open(ANSWERS_FILE, 'r') as file:
        f_data = file.readlines()

    f_data.append(','.join(data) + '\n')

    with open(ANSWERS_FILE, 'w') as file:
        file.writelines(f_data)

