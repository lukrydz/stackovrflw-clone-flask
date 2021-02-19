import uuid
import time

from data_handler import get_all_questions

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def generate_uuid():
    return uuid.uuid4()


def get_timestamp():
    return int(time.time())


def get_next_id():
    questions = get_all_questions()
    current_max = 0
    for question in questions:
        if int(question["id"]) >= current_max:
            current_max = int(question['id'])
    return current_max + 1


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
