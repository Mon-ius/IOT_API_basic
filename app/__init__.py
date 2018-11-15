import os
import logging
from flask import Flask, request, current_app
from ext import db, migrate, bootstrap, Config
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_restful import Api, Resource

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # DataBase init
    migrate.init_app(app, db)  # Database Migrate Init
    bootstrap.init_app(app)  # Bootstrap init

    from app.api import bp as api_bp  
    from app.api.routes import TemperatureAPI,TemperatureListAPI,LightAPI,LightListAPI,OpenRes

    api_temp = Api(api_bp)

    api_temp.add_resource(TemperatureListAPI, '/api/temps')
    api_temp.add_resource(TemperatureAPI, '/api/temps/<int:id>')
    api_temp.add_resource(LightListAPI, '/api/lights')
    api_temp.add_resource(LightAPI, '/api/lights/<int:id>')
    api_temp.add_resource(OpenRes, '/res')
    app.register_blueprint(api_bp)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    if not app.debug and not app.testing:

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/iotapi.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('*'*45)
        app.logger.info('*'*3+'    '*3+'IOT_API Startup'+'    '*3+'*'*3)
        app.logger.info('*'*45)
    return app




from app import models
