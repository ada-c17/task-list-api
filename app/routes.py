from flask import Blueprint
from os import abort
from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import asc, desc
import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix = "/goals")

#CREATE 
#task post route
@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    if "title" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    if "description" not in request_body:
        return {
            "details": "Invalid data"
        }, 400

    if "completed_at" not in request_body:
        completed_at = None
    else:
        completed_at = request_body["completed_at"]
    
    new_task = Task(
                title=request_body["title"],
                description=request_body["description"],
                completed_at=completed_at)


    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_dict()
    }, 201 

#goal post route
@goals_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    
    new_goal = Goal(
                title=request_body["title"])


    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }, 201 

#READ
#task get routes
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    param = request.args
    if "sort" in param:
        if param["sort"] == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif param["sort"] == "desc":
            tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    
    response = { "task": chosen_task.to_dict()}

    if chosen_task.goal_id:
        response ={ "task": {
                "id": chosen_task.task_id,
                "goal_id": chosen_task.goal_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)
                }
            }
    return jsonify(response), 200


#goal get routes
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.goal_id,
                "title": goal.title
            }
        )

    return jsonify(goals_response), 200



@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    chosen_goal = get_goal_or_abort(goal_id)
    
    response = { 
        "goal": {
                "id" : chosen_goal.goal_id,
                "title": chosen_goal.title
                }
            }
    return jsonify(response), 200



#UPDATE
#task update route
@tasks_bp.route("/<task_id>", methods=["PUT"])
def replace_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    request_body = request.get_json()

    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
        
    except KeyError:
        return {
            "details": "Invalid data"
        } , 400

    db.session.commit()

    return { "task": {
                "id" : chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)
                }
            }
    return jsonify(response), 200


#goal update route
@goals_bp.route("/<goal_id>", methods=["PUT"])
def replace_one_goal(goal_id):
    chosen_goal = get_goal_or_abort(goal_id)
    request_body = request.get_json()

    try:
        chosen_goal.title = request_body["title"]
        
    except KeyError:
        return {
            "details": "Invalid data"
        } , 400

    db.session.commit()

    return { "goal": {
                "id" : chosen_goal.goal_id,
                "title": chosen_goal.title
                }
            }
    return jsonify(response), 200


#PATCH
#task patch routes
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def completed_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    
    chosen_task.completed_at = datetime.datetime.utcnow()

    db.session.add(chosen_task)
    db.session.commit()

    post_message = f"Someone just completed the task {chosen_task.title}"

    path = "https://slack.com/api/chat.postMessage"
    key = os.environ.get('SLACK_TOKEN_KEY')
    data = {"channel": "task-notifications", "text": post_message}
    headers = {"Authorization": "Bearer " + key}

    response = requests.post(path, params=data, headers=headers)
    response_body = response.json()
    print(response_body)


    return { "task": {
                "id" : chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)
                }
            }, 200
    # return jsonify(response), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incompleted_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    chosen_task.completed_at = None

    db.session.add(chosen_task)
    db.session.commit()

    return { "task": {
                "id" : chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)
                }
            }, 200



#DELETE
#task delete route
@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f"Task {chosen_task.task_id} \"Go on my daily walk 🏞\" successfully deleted" }, 200

#goal delete route

@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_task(goal_id):
    chosen_goal = get_goal_or_abort(goal_id)
    db.session.delete(chosen_goal)
    db.session.commit()

    return {
        "details": f"Goal {chosen_goal.goal_id} \"Build a habit of going outside daily\" successfully deleted"}, 200



#helper function to handle invalid task id and no task in DB
#task input validation helper function
def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"details": "Invalid data"}
        abort(make_response(jsonify(response),400))

    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        response = {"message":f"Could not find task with id {task_id}"}
        abort(make_response(jsonify(response),404))
    return chosen_task

#goal input validation helper function
def get_goal_or_abort(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response = {"details": "Invalid data"}
        abort(make_response(jsonify(response),400))

    chosen_goal = Goal.query.get(goal_id)

    if chosen_goal is None:
        response = {"message":f"Could not find goal with id {goal_id}"}
        abort(make_response(jsonify(response),404))
    return chosen_goal

# gets one goal per task objects 
@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def add_tasks_to_goal(goal_id):
    goal = Goal.query.get(goal_id)
    request_body = request.get_json()
    task_list = []
    for task_id in request_body["task_ids"]:
        task_list.append(Task.query.get(task_id))
    
    goal.tasks = task_list

    db.session.commit()
    response = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }

    return make_response(jsonify(response), 200)




@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks_of_one_goal(goal_id):

    goal = get_goal_or_abort(goal_id)

    tasks_response = []

    for task in goal.tasks:
            tasks_response.append(
                {
                    "id": task.task_id,
                    "goal_id": goal.goal_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": bool(task.completed_at)
                }    
        )
            
    return jsonify({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": tasks_response}), 200

