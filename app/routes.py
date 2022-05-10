from attr import validate
from flask import Blueprint, jsonify, request, abort, make_response
import requests
import sqlalchemy
from app import db
from app.models.task import Task
from app.models.goal import Goal
import sqlalchemy
import datetime
import os




task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {task_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        rsp = {"msg": f"Could not find task with id {task_id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_task

@task_bp.route("", methods = ["POST"])
def create_new_task():
    request_body = request.get_json()
    
    try:
        title = request_body["title"]
        description = request_body["description"]
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
    )
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": False
    }
    }), 201

@task_bp.route("", methods=["GET"])
def get_all_task():
    sort_query = request.args.get("sort")
    response = []
    tasks = Task.query.all()
    
    if sort_query == "desc":
        tasks = Task.query.order_by(sqlalchemy.desc(Task.title))
    elif sort_query == "asc":
        tasks = Task.query.order_by(sqlalchemy.asc(Task.title))
        
    for task in tasks:
        response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        )
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):    
    chosen_task = validate_id(task_id)
    return jsonify(
        {
        "task": {
        "id": chosen_task.task_id,
        "title": chosen_task.title,
        "description": chosen_task.description,
        "is_complete": False
        },
}), 200

@task_bp.route("/<task_id>", methods=["PUT"])
def replace_one_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify({'msg': f"Invalid task id: '{task_id}'. ID must be an integer"}), 400

    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({'msg': f"Request must include title, description, and is_complete"}), 400

    chosen_task = Task.query.get(task_id)
    
    if chosen_task is None:
        return jsonify({'msg': f'Could not find task with id {task_id}'}), 404

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]


    db.session.commit()

    return make_response(
        jsonify({
            "task": {
            "id": chosen_task.task_id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": False
        }
        }
                )), 200
    
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify({'msg': f"Invalid task id: '{task_id}'. ID must be an integer"}), 400

    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'msg': f'Could not find task with id {task_id}'}), 404

    db.session.delete(task)
    db.session.commit()


    rsp = {"details": f'Task {task_id} "{task.title}" successfully deleted'}
    
    return jsonify(rsp), 200

@task_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_complete_incomplete_task(task_id):
    task = validate_id(task_id)
    task.completed_at = datetime.datetime.now()
    db.session.commit()
    
    SLACK_URL = 'https://slack.com/api/chat.postMessage'
    authorization = os.environ.get('SLACK_BOT_TOKEN')
    slack_msg = {"text": f"Someone just completed the task {task.title}", "channel" : "C03ERFMNXC2"}
    requests.post(SLACK_URL, json = slack_msg, headers = {'Authorization': f'Bearer {authorization}'})
    
    return jsonify({
        "task":{
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": True
        }
        }), 200

@task_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_incomplete_complete_task(task_id):
    task = validate_id(task_id)
    task.completed_at = None
    db.session.commit()

    return jsonify({
        "task":{
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
        }}), 200
    
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals") 

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {goal_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_goal = Goal.query.get(goal_id)

    if chosen_goal is None:
        rsp = {"msg": f"Could not find task with id {goal_id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_goal


@goal_bp.route("", methods = ["POST"])
def create_new_goal():
    request_body = request.get_json()

    try:
        title = request_body["title"]
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    if title not in request_body:
        rsp = {"details": "Invalid data"}
        return jsonify(rsp), 400
    
    new_goal = Goal(
        title = request_body["title"])

    db.session.add(new_goal)
    db.session.commit()
    
    return jsonify(
        {
        "goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title
        }}), 201
    
@goal_bp.route("", methods=["GET"])
def get_all_goal():
    response = []
    goals = Goal.query.all()
        
    for goal in goals:
        if goal not in goals:
            return jsonify([])
        response.append(
            {
                "id": goal.goal_id,
                "title": goal.title,
            })
    return jsonify(response), 200
 
    
@goal_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):      
    chosen_goal = validate_goal(goal_id)
    return jsonify({
        "goal":{
        "id": chosen_goal.goal_id,
        "title": chosen_goal.title
        }}), 200
    
@goal_bp.route("/<goal_id>", methods=["PUT"])
def replace_one_goal(goal_id):
    request_body = request.get_json()

    chosen_goal = validate_goal(goal_id)
    chosen_goal.title = request_body["title"]
    db.session.commit()

    return make_response(
        jsonify({
        "title": chosen_goal.title
        })), 200
    
@goal_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_one_task(goal_id):
    chosen_goal = validate_goal(goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()


    rsp = {"details": f'Goal {chosen_goal.goal_id} {chosen_goal.title} successfully deleted'}
    
    return jsonify(rsp), 200
