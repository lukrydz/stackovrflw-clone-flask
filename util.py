import uuid
import datetime
import bcrypt

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def generate_uuid():
    return uuid.uuid4()


def get_timestamp():
    return datetime.datetime.now()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def hash_password(password):
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)