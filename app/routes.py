from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy.sql import text
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from app.models.goal import Goal

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):

    goal = validate_object("goal", goal_id)

    request_body = request.get_json()

    for task in request_body["task_ids"]:
        task = validate_object("task", task)
        task.goal_id = goal_id

    db.session.commit()

    tasks = []

    for task in goal.tasks:
        tasks.append(task.task_id)
        
    response = {
        "id" : goal.goal_id,
        "task_ids" : tasks
    }

    return make_response(jsonify(response), 200)    



@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_by_goals(goal_id):

    goal = validate_object("goal", goal_id)

    response = goal.to_json(category="tasks")

    return make_response(jsonify(response), 200)    





@goals_bp.route("", methods=["POST"])
def create_one_goal():

    request_body = request.get_json()

    try:
        new_goal = Goal.create(request_body)
    except KeyError:
        return make_response(jsonify({"details" : "Invalid data"}), 400)

    db.session.add(new_goal)
    db.session.commit()

    response = { "goal": new_goal.to_json()}

    return make_response(response, 201)



@goals_bp.route("", methods=["GET"])
def read_all_goals():
    title_query = request.args.get("sort")

    if title_query:
        goals = Goal.query.order_by(text(f'title {title_query}'))
    else:
        goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(
            goal.to_json()
        )
    return make_response(jsonify(goals_response), 200)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_object("goal", goal_id)

    response = { "goal": goal.to_json()}

    return make_response(response, 200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):

    goal = validate_object("goal", goal_id)

    request_body = request.get_json()

    goal.update(request_body)

    db.session.commit()

    response = { "goal": goal.to_json()}
    return make_response(response, 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):

    goal = validate_object("goal", goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details" : f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}))


@tasks_bp.route("", methods=["POST"])
def create_task():

    request_body = request.get_json()
    try:
        new_task = Task.create(request_body)
    except KeyError:
        return make_response(jsonify({"details" : "Invalid data"}), 400)

    if request_body.get("completed_at"):
        new_task.is_complete = True
        new_task.completed_at = datetime.now()

    db.session.add(new_task)
    db.session.commit()

    response = { "task": new_task.to_json()}

    return make_response(response, 201)



@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get("sort")

    if title_query:
        tasks = Task.query.order_by(text(f'title {title_query}'))
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            task.to_json()
        )
    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_object("task", task_id)

    response = { "task": task.to_json()}

    return make_response(response, 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):

    task = validate_object("task", task_id)

    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    response = { "task": task.to_json()}
    return make_response(response, 200)



@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):

    task = validate_object("task", task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details" : f"Task {task.task_id} \"{task.title}\" successfully deleted"}))


@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_task_completed(task_id):
    task = validate_object("task", task_id)

    task.is_complete = True
    task.completed_at = datetime.now()

    db.session.commit()

    URL = "https://slack.com/api/chat.postMessage"
    PARAMS = {'text' : f"Someone just completed the task {task.title}",
    'channel' : 'task-notifications'}
    HEADERS = {'Authorization' : f'Bearer {os.environ.get("TASKLIST_BOT_KEY")}'}
    r = requests.get(url = URL, params = PARAMS, headers = HEADERS)

    response = { "task": task.to_json()}

    return response, 200

    
@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incompleted(task_id):
    task = validate_object("task", task_id)

    task.is_complete = False
    task.completed_at = None

    db.session.commit()

    response = { "task": task.to_json()}

    return response, 200





def validate_object(object_type, object_id):

    try:
        object_id = int(object_id)
    except:
        abort(make_response({"message":f"{object_type} {object_id} invalid"}, 400))

    if object_type == "task":
        item = Task.query.get(object_id)
    elif object_type == "goal":
        item = Goal.query.get(object_id)

    if not item:
        abort(make_response({"message":f"{object_type} {object_id} not found"}, 404))

    return item


