from flask import Blueprint, jsonify, request, make_response, abort, Flask
from app.models.task import Task
from app.models.goal import Goal
import os
import requests

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"goal {goal_id} not found"}, 404))

    return goal


def call_slack(response_message):
    
    path = "https://slack.com/api/chat.postMessage"

    #Headers = {"Authorization": os.environ.get("SLACK_TOKEN")}
    Headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"
    }
    query_params = {
        "channel": "task-notifications",
        "text": response_message
    }
    response = requests.post(path, data=query_params, headers=Headers)
    #return response.json()
    # print(f"Someone just completed poppy's task {title}")

    # def create_app(test_config=None):
    #      app = Flask(__name__)

    #      app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #      if not test_config:
    #      app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    #     "SQLALCHEMY_DATABASE_URI")
    #      else:
    #      app.config["TESTING"] = True
    #      app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    #     "SQLALCHEMY_TEST_DATABASE_URI")

    #      db.init_app(app)
    #      migrate.init_app(app, db)

    #      from app.models.planet import Planet

    #      from .routes import solar_bp
    #      app.register_blueprint(solar_bp)

    #      return app
