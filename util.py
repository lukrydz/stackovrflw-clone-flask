import uuid
import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def generate_uuid():
    return uuid.uuid4()


def get_timestamp():
    return datetime.datetime.now()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
