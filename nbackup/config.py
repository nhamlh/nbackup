from os import path

DEBUG = True

SECRET_KEY = 'verylongandsecuresecretkey'

SQLALCHEMY_DATABASE_URI = 'postgresql://nbackup:password@localhost/nbackup'

_BASE_DIR_ = path.dirname(path.abspath(__file__))
