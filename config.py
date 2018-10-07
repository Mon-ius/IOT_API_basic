import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                'dasdaa13as12SQ'
    BOOTSTRAP_SERVE_LOCAL = False
    ADMINS = os.environ.get('ADMIN_MAIL') or ['your-email@example.com']
    POSTS_PER_PAGE = 25


