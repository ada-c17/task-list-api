from sqlalchemy import asc, desc
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime
import requests
import os


tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id) 
    except:
        abort(make_response({"details":f"Invalid data"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task

def convert_task_to_dict(task):
    task_dict = task.to_dict()
    return task_dict


@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title = request_body['title'],
                        description = request_body['description'])
    except:
        abort(make_response({"details":f"Invalid data"}, 400))
    
    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": bool(new_task.completed_at)
    }
},201

@tasks_bp.route('', methods=['GET'])
def list_all_tasks():
    task_query = request.args.get("sort")
    if task_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif task_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()
    task_response = []
    for task in tasks:
        task_response.append(
            {
                "id":task.task_id,
                "title":task.title,
                "description":task.description,
                "is_complete": False 
            }
        )
    return jsonify(task_response)

@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)
    return {
                "task": {
                "id":task.task_id,
                "goal_id":task.goal_id,
                "title":task.title,
                "description":task.description,
                "is_complete": False 
            }
    }

@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_one_task(task_id, ):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]
    

    db.session.commit()
    return{
                "task": {
                "id":task.task_id,
                "title":task.title,
                "description":task.description,
                "is_complete": bool(task.completed_at)
            }
    }

@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    task= validate_task(task_id)

    db.session.delete(task)
    db.session.commit()
    return {'details': f'Task {task.task_id} "{task.title}" successfully deleted'}

@tasks_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
def complete_one_task(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.utcnow()
    headers= {'Authorization': os.environ.get('SLACKBOT_TOKEN')}
    specs = {'channel': 'task-notifications',
    'text': f'Someone just completed the task {task.title}'}
    slack_response = requests.post('https://slack.com/api/chat.postMessage', 
    headers=headers, params=specs)
    db.session.commit()
    return{
                "task": {
                "id":task.task_id,
                "title":task.title,
                "description":task.description,
                "is_complete": True 
            }
    }

@tasks_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def fail_one_task(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()
    return{
                "task": {
                "id":task.task_id,
                "title":task.title,
                "description":task.description,
                "is_complete": False 
            }
    }

########################routes for goals below###############################

goals_bp = Blueprint("goals", __name__, url_prefix = "/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id) 
    except:
        abort(make_response({"details":f"Invalid data"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"goal {goal_id} not found"}, 404))

    return goal


@goals_bp.route('', methods=['POST'])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title = request_body['title']
    )
    except:
        abort(make_response({"details":f"Invalid data"}, 400))
    
    db.session.add(new_goal)
    db.session.commit()
    return {
        "goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title,
    }
},201


@goals_bp.route('', methods=['GET'])
def list_all_goals():
    goals = Goal.query.all()
    goal_response = []
    for goal in goals:
        goal_response.append(
            {
                "id":goal.goal_id,
                "title":goal.title
            }
        )
    return jsonify(goal_response)

@goals_bp.route("/<goal_id>", methods=['GET'])
def get_a_goal(goal_id):
    goal = validate_goal(goal_id)
    return {
                "goal": {
                "id":goal.goal_id,
                "title":goal.title,
            }
    }

@goals_bp.route("/<goal_id>", methods=['PUT'])
def update_one_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()
    return{
                "goal": {
                "id":goal.goal_id,
                "title":goal.title,
            }
    }

@goals_bp.route("/<goal_id>", methods=['DELETE'])
def delete_goal(goal_id):
    goal= validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()
    return {
        "details": f'Goal {goal_id} "Build a habit of going outside daily" successfully deleted'
    }


@goals_bp.route("/<goal_id>/tasks", methods =['POST'])
def add_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()
    try:
        task_ids = request_body["task_ids"]
    except KeyError:
        return jsonify({'msg': "Missing task_ids in request body"}), 400

    if not isinstance(task_ids, list):
        return jsonify({'msg': "Expected list of task ids"}), 400

    tasks = []
    for id in task_ids:
        tasks.append(validate_task(id))
        
    tasks_with_goal = []
    for task in tasks:
        task.goal = goal
        tasks_with_goal.append(task.task_id)

    db.session.commit()

    return jsonify({
            "id": goal.goal_id,
            "task_ids": tasks_with_goal
    }), 200

@goals_bp.route("/<goal_id>/tasks", methods =['GET'])
def get_goal_with_tasks(goal_id):
    goal = validate_goal(goal_id)
    task_dics = []
    for task in goal.tasks:
        converted_task =convert_task_to_dict(task)
        task_dics.append(converted_task)
    return {
                "id" :goal.goal_id,
                "title" :goal.title,
                "tasks" : task_dics
            
    }