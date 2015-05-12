import os

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = 'Focus'

ADMIN_USER = "admin"
ADMIN_PWD = "admin"
DEBUG = True
SECRET_KEY = b'.\x0c;1\x81\xb7lq\xf2\xd1\xc4pV\x10\x8b6\x7fi\xac\xd2'

# The list of allowed extensions of upload
UPLOAD_ALLOWED = "jpg jpeg gif png bmp webm txt".split()
UPLOAD_FOLDER = os.path.abspath(os.path.expandvars(os.path.expanduser("upload")))
