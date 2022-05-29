from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)

    from .routes.goals import goals_bp
    app.register_blueprint(goals_bp)

    @app.errorhandler(404)
    def pageNotFound(error):
        return "<h1> Page not found </h1>", 404 

    @app.route("/")
    @app.route("/main")
    @app.route("/index")
    @app.route("/about")
    def about():
        return "<h1> The Task List Project by: Nina Patrina. Ada Developers Academy, 2022 </h1>"    
    
    return app
