import sqlalchemy
from sqlalchemy import desc,and_
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import Config
from flask_httpauth import HTTPBasicAuth

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
auth = HTTPBasicAuth()
