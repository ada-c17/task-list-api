
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # db.init_app(app)
    # migrate.init_app(app, db)        

    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal

    db.init_app(app)
    migrate.init_app(app, db)  
    
    from .routes import task_bp, goal_bp
    app.register_blueprint(task_bp)
    app.register_blueprint(goal_bp)
    # app.register_blueprint(main_bp)



    # Register Blueprints here
    CORS(app)
    return app
