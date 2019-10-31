import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
class Config(object):
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URLs')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                'dasdaa13as12SQ'
    BOOTSTRAP_SERVE_LOCAL = False
    ADMINS = os.environ.get('ADMIN_MAIL') or ['your-email@example.com']
    POSTS_PER_PAGE = 25


