import csv
import os


QUESTION_FILE = 'sample_data/question.csv'
DATA_HEADER = ['id','submission_time','view_number','vote_number','title','message','image']


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


def get_next_id():
    questions = get_all_questions()
    current_max = 0
    for question in questions:
        if int(question["id"]) >= current_max:
            current_max = int(question['id'])
    return current_max + 1