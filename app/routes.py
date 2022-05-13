from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort, Response
from app.helper_routes import error_message
import os 
from datetime import datetime
import requests



slack_url = "https://slack.com/api/chat.postMessage"
slack_bot_token= os.environ.get("SLACK_BOT_TOKEN")



task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")





@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    response_body = [goal.to_dict() for goal in goals]
    return jsonify(response_body)
    


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_tasks = request.args.get('sort')
  
    if not sort_tasks: 
        tasks = Task.query.all()
    elif sort_tasks == "asc": 
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_tasks == "desc": 
        tasks = Task.query.order_by(Task.title.desc()).all()
    else: 
        tasks = Task.query.all()

    response_body = [task.to_dict() for task in tasks]
    return jsonify(response_body)

@goal_bp.route("/<id>/tasks", methods=["GET"])
def get_tasks_for_goal(id):
    goal = validate_goal(id)

    task_of_goal = []

    goal_with_tasks = {"id": goal.id,
    "title": goal.title,
    "tasks": task_of_goal}

    
    for task in goal.tasks: 
        task = validate_task(id)
        
        task_of_goal.append(task.to_dict())

    print(goal_with_tasks, "MY ANS!!!")

    return goal_with_tasks


def validate_task(id):
	try:
		id = int(id)
	except ValueError:
		error_message(f"Invalid id {id}", 400)

	task = Task.query.get(id)
		
	if task:
		return task
	error_message(f'task with id #{id} not found', 404)

def validate_goal(id):
	try:
		id = int(id)
	except ValueError:
		error_message(f"Invalid id {id}", 400)

	goal = Goal.query.get(id)
		
	if goal:
		return goal
	error_message(f'Goal with id #{id} not found', 404)

def make_task_safely(data_dict):
    return Task.from_dict(data_dict)


@goal_bp.route("", methods=["POST"]) 
def create_goal(): 
    request_body= request.get_json() 

    if "title" not in request_body:
        return {'details': 'Invalid data'}, 400

    new_goal = Goal(
        title = request_body.get("title"))
        
    db.session.add(new_goal)
    db.session.commit()
    return {"goal": new_goal.to_dict()}, 201  



    


@task_bp.route("", methods=["POST"])
def create_task():  
    request_body = request.get_json() 
    

    # return request_body  
    if "title" not in request_body or "description" not in request_body:
        return {'details': 'Invalid data'}, 400

    new_task = Task(
        title = request_body.get("title"),
        description = request_body.get("description"),
        # is_complete=True if "completed_at" in request_body else False 
        ) 
    # if "completed_at" in request_body: 
    #     new_task.is_complete=request_body['is_complete']

    print("new_task", new_task)
        
    db.session.add(new_task)
    db.session.commit()
    return {"task": new_task.to_dict()}, 201 


@task_bp.route("/<id>", methods=["GET"])
def get_task(id):
    task = validate_task(id)
    response_body = {"task": task.to_dict()}
    return response_body 

@goal_bp.route("/<id>", methods=["GET"]) 
def get_goal(id):
    goal = validate_goal(id)
    return {"goal": goal.to_dict()}



def replace_task_safely(task, data_dict):
    return task.replace_details(data_dict)



@task_bp.route("/<id>", methods=["PUT"])
def update_task_by_id(id):
    request_body = request.get_json()
    task = validate_task(id)
    
    replace_task_safely(task, request_body)
    db.session.add(task)
    db.session.commit()
    return {"task": task.to_dict()}

@goal_bp.route("/<id>", methods=["PUT"])
def update_goal_by_id(id):
    goal = validate_goal(id)
    request_body = request.get_json()

    goal.title = request_body['title']
    
    db.session.add(goal)
    db.session.commit()
    return {"goal": goal.to_dict()}
    
@goal_bp.route("/<id>/tasks", methods=["POST"])
def tasks_of_goal(id): 
    goal = validate_goal(id)
    request_body = request.get_json()

    for id in request_body['task_ids']: 
        new_task = validate_task(id)
        goal.tasks.append(new_task)

    db.session.commit()
    return {"id": goal.id, 
    "task_ids" : request_body['task_ids']}
        
        
        
@task_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = validate_task(id)
    task.is_complete = True 
    task.completed_at = datetime.utcnow()

    db.session.commit()
    headers = {
        "Authorization": f"Bearer {slack_bot_token}",
    }
    data = {
        "channel": "test-channel",
        "text": "Task {task.title} has been marked complete",
    }

    return {"task": task.to_dict()}

@task_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = validate_task(id)
    task.completed_at = None
    task.is_complete = False
    

    db.session.commit()
    headers = {
        "authorization": f"Bearer {slack_bot_token}",
    }
    data = {
        "channel": "test-channel",
        "text": f"Task {task.title} is not complete",
    }
    return {"task": task.to_dict()}


@task_bp.route("/<id>", methods=["DELETE"])
def delete_task(id): 
    task = validate_task(id)

    response_body = {"details": f'Task {task.id} "{task.title}" successfully deleted'}

    db.session.delete(task)
    db.session.commit()
    return response_body



@goal_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id): 
    goal = validate_goal(id)

    response_body = {"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}

    db.session.delete(goal)
    db.session.commit()
    return response_body






     

  


  



