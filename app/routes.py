from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import requests



tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_task_id(task_id):
    
    try:
        task_id = int(task_id)
    except ValueError:
        response_msg = {"message": f'{task_id} id is not valid, must be an integer'}
        abort(make_response(jsonify(response_msg), 400))
    the_task = Task.query.get(task_id)

    
    if the_task is None:
        response_msg = {"message": f'task with id {task_id} not found'}
        abort(make_response(jsonify(response_msg), 404))
    return the_task

   

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    if "completed_at" in request_body: 
    # /and isinstance(request_body["completed_at"], datetime.date):
        new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"],
                    is_complete=True)
    else:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()


    return make_response(jsonify({"task":{
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.is_complete
    }
    }), 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    param = request.args.get("sort")
    
    tasks_response = []
    
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        })
    if param == "asc":
        tasks_response = sorted(tasks_response, key=lambda d: d["title"])
    if param == "desc":
        tasks_response = sorted(tasks_response, key=lambda d: d["title"], reverse=True)
    
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):

    task = validate_task_id(task_id)

    if task.goal_id is None:
        return jsonify({"task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
            }})
    else:
        return jsonify({"task":{
            "goal_id": task.goal_id,
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
            }})


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task_id(task_id)

    request_body = request.get_json()

    if "completed_at" in request_body: 
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]
        task.is_complete = True
    
    else:
        task.title = request_body["title"]
        task.description = request_body["description"]
    # task.completed_at = request_body["completed_at"]
    # task.is_complete = request_body["is_complete"]

    db.session.commit()

    return jsonify({"task":{
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete
        }})

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task_id(task_id)

    db.session.delete(task)
    db.session.commit()

    task_deleted = f'Task {task.task_id} "{task.title}" successfully deleted'

    return make_response({"details": task_deleted})

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    
    task = validate_task_id(task_id)


    task.completed_at = datetime.utcnow()
    task.is_complete = True

    db.session.commit()
    
    requests.post(
        "https://slack.com/api/chat.postMessage",
        data={
            "channel":"general",
            "text": f'Someone just completed the task {task.title}'},
        headers={"Authorization": "Bearer TOKEN_FOR_SLACK xoxb-3530423669872-3509059378276-hi3GtBisjhstDiTw61KD2dFl"}
        )

    task_updated = {"task": {
    "id": task.task_id,
    "title": task.title,
    "description": task.description,
    "is_complete": task.is_complete
                            }
                    }
    return make_response(jsonify(task_updated), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task_id(task_id)

    task.completed_at = None
    task.is_complete = False

    db.session.commit()

    task_updated = {"task": {
    "id": task.task_id,
    "title": task.title,
    "description": task.description,
    "is_complete": task.is_complete
                            }
                    }

    return make_response(jsonify(task_updated),200)

########################################################################################
#####################  ""ROUTES FOR GOALS""  ##########################
########################################################################

def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response_msg = {"message": f'{goal_id} id is not valid, must be an integer'}
        abort(make_response(jsonify(response_msg), 400))
    the_goal = Goal.query.get(goal_id)

    if the_goal is None:
        response_msg = {"message": f'goal with id {goal_id} not found'}
        abort(make_response(jsonify(response_msg), 404))
    return the_goal

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)


    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()


    return make_response(jsonify({"goal":{
        "id": new_goal.goal_id,
        "title": new_goal.title
    }
    }), 201)

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    param = request.args.get("sort")
    
    goals_response = []
    
    goals = Goal.query.all()
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title
        })
    if param == "asc":
        goals_response = sorted(goals_response, key=lambda d: d["title"])
    if param == "desc":
        goals_response = sorted(goals_response, key=lambda d: d["title"], reverse=True)
    
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):

    goal = validate_goal_id(goal_id)

    return jsonify({"goal":{
        "id": goal.goal_id,
        "title": goal.title
        }})
    
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal_id(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal":{
        "id": goal.goal_id,
        "title": goal.title
        }})

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    goal_deleted = f'Goal {goal.goal_id} "{goal.title}" successfully deleted'

    return make_response({"details": goal_deleted})

# GET all tasks from a goal
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    
    goal = validate_goal_id(goal_id)
    #goal = {"title": "whatever", "goal_id"= number}
    
    request_body = request.get_json()

    task_ids = request_body["task_ids"]
    # [1, 3, 5] list of ids that belongs to a task

    tasks = []
    for task_id in task_ids:
        tasks.append(validate_task_id(task_id))
    #tasks = [{info task 1, info task 2...}]

    for task in tasks:
        task.goal_id = goal.goal_id

    db.session.commit()

    return make_response(jsonify({
        "id": goal.goal_id,
        "task_ids":request_body["task_ids"]
    }), 200)
    
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_goal_id(goal_id)
    #Goal object with id

    tasks = Task.query.all()
    #[Task1, Task2, Task...]

    tasks_from_goal = []
    for task in tasks:
        if task.task_id == goal.goal_id:
            tasks_from_goal.append({
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete
                })
    
    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_from_goal
    })


