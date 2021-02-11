from csv import reader

ID_INDEX = 0
SUBMISSION_TIME_INDEX = 1
VIEW_NUMBER = 2
VOTE_NUMBER = 3
TITLE_INDEX = 4
MESSAGE_INDEX = 5
IMAGE_INDEX = 6

QUESTIONS_FILE_PATH = 'data/question.csv'


def open_data_file(file):
    data = open(file)
    data_list = data.read().split("\n")
    data.close()
    return data_list


def open_counter_file():
    with open('data/counter.csv', "r") as file:
        return str(file.read())


def create_headers():
    data = open_data_file(QUESTIONS_FILE_PATH)
    return data[0]


def get_questions():
    questions = open(QUESTIONS_FILE_PATH, "r")

    questions_list = []
    for row in reader(questions):
        questions_list.append(row)
    return questions_list


for row in get_questions():
    print(row)


def create_counter():
    counter = 0
    return counter


def save_counter(counter):
    with open('data/counter.csv', "w") as counter_file:
        counter_file.write(str(counter))
