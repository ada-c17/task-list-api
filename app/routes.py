from datetime import datetime
from flask import Blueprint, jsonify, request, abort, make_response
import sqlalchemy
from app.models.task import Task
from app.models.goal import Goal
from app import db
import requests
from dotenv import load_dotenv
import os


load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@tasks_bp.route("", methods=["POST"])
def create_one_task():
    if not request.is_json:
        return {"msg" : "Missing JSON request body"}, 400
    
    request_body = request.get_json()
    try:
        title = request_body["title"]
        description = request_body["description"]
    except KeyError:
        return {"details": "Invalid data"}, 400

    new_task = Task(title=title,
                description=description,
                completed_at=request_body["completed_at"] if "completed_at" in request_body else None)

    db.session.add(new_task)
    db.session.commit()
    
    rsp = {"task" : new_task.get_dict()}

    return jsonify(rsp), 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    tasks = Task.query.all()
    
    if sort_query == "desc":
        tasks = Task.query.order_by(sqlalchemy.desc(Task.title))
    elif sort_query == "asc":
        tasks = Task.query.order_by(sqlalchemy.asc(Task.title))

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.get_dict())
    
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    rsp = {"task" : task.get_dict()}

    return jsonify(rsp), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)

    if not request.is_json:
        return {"msg" : "Missing JSON request body"}, 400

    request_body = request.get_json()
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except KeyError:
        return {
            "msg" : "Update failed due to missing data. Title, Description are required!"
        }, 400

    db.session.commit()

    rsp = {"task" : task.get_dict()}
    return jsonify(rsp), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    rsp = {"details": f'Task {task_id} "{task.title}" successfully deleted'}
    return jsonify(rsp), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    SLACK_URL = 'https://slack.com/api/chat.postMessage'
    msg_to_post = {"text": f"Someone just completed the task {task.title}", "channel" : "C03EF25FZNW"}
    auth = os.environ.get('SLACK_BOT_TOKEN')
    requests.post(SLACK_URL, json=msg_to_post, headers={'Authorization': f'Bearer {auth}'})

    rsp = {"task" : task.get_dict()}
    return jsonify(rsp), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None

    db.session.commit()
    
    rsp = {"task" : task.get_dict()}
    return jsonify(rsp), 200


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        rsp = {"msg" : f"Task with id #{task_id} is invalid."}
        abort(make_response(rsp, 400))
    
    task = Task.query.get(task_id)

    if not task:
        rsp = {"msg" : f"Task with id #{task_id} is not found!"}
        abort(make_response(rsp, 404))
    return task


@goals_bp.route("", methods=["POST"])
def create_one_goal():
    if not request.is_json:
        return {"msg" : "Missing JSON request body"}, 400
    
    request_body = request.get_json()
    try:
        title = request_body["title"]
    except KeyError:
        return {"details": "Invalid data"}, 400

    new_goal = Goal(title=title)

    db.session.add(new_goal)
    db.session.commit()
    
    rsp = {"goal" : new_goal.get_dict()}

    return jsonify(rsp), 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    sort_query = request.args.get("sort")
    goals = Goal.query.all()
    
    if sort_query == "desc":
        goals = Goal.query.order_by(sqlalchemy.desc(Goal.title))
    elif sort_query == "asc":
        goals = Goal.query.order_by(sqlalchemy.asc(Goal.title))

    goals_response = []
    for goal in goals:
        goals_response.append(goal.get_dict())
    
    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    rsp = {"goal" : goal.get_dict()}

    return jsonify(rsp), 200


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        rsp = {"msg" : f"Goal with id #{goal_id} is invalid."}
        abort(make_response(rsp, 400))
    
    goal = Goal.query.get(goal_id)

    if not goal:
        rsp = {"msg" : f"Goal with id #{goal_id} is not found!"}
        abort(make_response(rsp, 404))
    return goal


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_goal(goal_id)

    if not request.is_json:
        return {"msg" : "Missing JSON request body"}, 400

    request_body = request.get_json()
    try:
        goal.title = request_body["title"]
    except KeyError:
        return {
            "msg" : "Update failed due to missing data. Title is required!"
        }, 400

    db.session.commit()

    rsp = {"goal" : goal.get_dict()}
    return jsonify(rsp), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    rsp = {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
    return jsonify(rsp), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task_for_specific_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    task_ids = request_body["task_ids"]

    for id in task_ids:
        task = Task.query.get(id)
        if not id in goal.tasks:
            task.goal = goal

    db.session.commit()
    
    rsp = { "id": goal.goal_id, "task_ids": task_ids}
    return jsonify(rsp), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_goal(goal_id)

    all_tasks = []

    for task in goal.tasks:
        all_tasks.append(task.get_dict())

    rsp = {
        "id" : goal.goal_id,
        "title" : goal.title,
        "tasks": all_tasks
    }

    return jsonify(rsp), 200
    