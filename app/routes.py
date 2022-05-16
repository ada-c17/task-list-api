from app.models.task import *
from app.models.goal import *
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import date
import requests
import os
from dotenv import load_dotenv
load_dotenv()
slack_token = os.environ.get("SLACK_TOKEN")

# This is the BluePrint object that helps to "connect" my functions to
# endpoints and HTTP methods for tasks.
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

#---------------post_task-----------
# This function will be invoked when Flask receives an HTTP request with:
#   method = POST
#   endpoint = "/tasks"
# This function creates a new Task instance with the information the client included
# in the HTTP request. I get this information by using the global "request" variable.
@tasks_bp.route("", methods=["POST"])
def post_task():
    # request.get_json() returns a dictionary with keys: "title", "description"
    # Use corresponding values to create the Task instance.
    post_dict = request.get_json()
    print(post_dict)
    if 'title' not in post_dict or 'description' not in post_dict:
        return make_response({"details":"Invalid data"},400)
    if 'completed_at' not in post_dict:
        completed_at = None
    else:
        completed_at = post_dict['completed_at']
    
    title = post_dict['title']
    description = post_dict['description']

    task = Task(title=title, description=description, completed_at = completed_at)
    db.session.add(task)
    db.session.commit()

    task_dict={}
    if completed_at == None:
        task_dict['is_complete'] = False
    else:
        task_dict['is_complete'] = True
        

    task_dict['id'] = task.id
    task_dict['title'] = task.title
    task_dict['description'] = task.description
    return_dict = {"task": task_dict}
    return jsonify(return_dict), 201

# -------------get_all_tasks--------------
# This function returns a list of dictionaries,
# where each dictionary has keys: "id", "title", "description", "completed_data"
# and values from a Task instance in the task_db.
@tasks_bp.route("", methods=["GET"]) 
def get_all_tasks():
    
    sort_query = request.args.get('sort')
    if sort_query == 'asc':
        task_db = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == 'desc':
        task_db = Task.query.order_by(Task.title.desc()).all()
    else:
        task_db = Task.query.all()
    
    tasks_response = []
    for task in task_db:
        if task.completed_at == None:
            is_complete = False
        else:
            is_complete = True
        
        task_dict = {'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'is_complete': is_complete}
        tasks_response.append(task_dict)
    
    return jsonify(tasks_response), 200    

# -------get task by id--------------------    

# This function finds the task with matching ID.
# If a matching task is found, it return a dictionary with keys: "id", "title", "description", "completed_at"
# and values from the matching Task instance.
# If there is no matching task, then return an error message with return code 404
@tasks_bp.route("/<id>",methods = ["GET"]) 
def get_task_by_id(id):
    # Remember that id from the request is a string and not an integer

    task = Task.query.get(id)
    if (task == None):
        abort(make_response({"message":f"task {id} not found"}, 404))
    
    if task.completed_at == None:
        is_complete = False
    else:
        is_complete = True
    
    task_dict={}
    task_dict['id'] = task.id
    task_dict['title'] = task.title
    task_dict['description'] = task.description
    task_dict['is_complete'] = is_complete
    if not (task.goal_id == None):
        task_dict['goal_id'] = task.goal_id
    return_dict = {"task": task_dict}
    return jsonify(return_dict), 200

#------------remove task by id------------
@tasks_bp.route("/<id>", methods=["DELETE"])
def remove_task_by_id(id):
    task = Task.query.get(id)
    
    if (task == None):
        abort(make_response({"message":f"task {id} not found"}, 404))
    
    db.session.delete(task)
    db.session.commit()
    return make_response({"details":f"Task {id} \"{task.title}\" successfully deleted"},200)
    

#------------PUT Method - update task by id---------
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task_by_id(id):
    task = Task.query.get(id)

    if (task == None):
        abort(make_response({"message":f"task {id} not found"}, 404))

    update_dict = request.get_json()
    
    if 'title' not in update_dict or 'description' not in update_dict:
        return make_response({"details":"Invalid data"},400)
    
    if 'completed_at' not in update_dict:
        completed_at = None
    else:
        completed_at = update_dict['completed_at']
    
    title = update_dict['title']
    description = update_dict['description']

    task.title = title
    task.description = description
    task.completed_at = completed_at
    db.session.commit()

    task_dict={}

    if completed_at == None:
        task_dict['is_complete'] = False
    else:
        task_dict['is_complete'] = True

    task_dict['id'] = task.id
    task_dict['title'] = task.title
    task_dict['description'] = task.description
    
    return_dict = {"task": task_dict}
    return jsonify(return_dict), 200

#------------PUT Method - update task by id - Mark_complete---------
def send_slack_message(task_title):
    params = {"channel":"task-notifications","text":task_title}
    headers = {"Authorization":"Bearer " + slack_token}
    requests.post("https://slack.com/api/chat.postMessage", params=params, headers=headers)

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def patch_completed_task_by_id(id):
    task = Task.query.get(id)

    if (task == None):
        abort(make_response({"message":f"task {id} not found"}, 404))

    
    task.completed_at = date.today()
    
    db.session.commit()

    send_slack_message(task.title)

    task_dict={}
    task_dict['id'] = task.id
    task_dict['title'] = task.title
    task_dict['description'] = task.description
    task_dict['is_complete'] = True
    return_dict = {"task": task_dict}
    return jsonify(return_dict), 200

#------------PUT Method - update task by id - Mark_Incomplete---------
@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def patch_incomplete_task_by_id(id):
    task = Task.query.get(id)

    if (task == None):
        abort(make_response({"message":f"task {id} not found"}, 404))

    
    task.completed_at = None
    
    db.session.commit()

    task_dict={}
    task_dict['id'] = task.id
    task_dict['title'] = task.title
    task_dict['description'] = task.description
    task_dict['is_complete'] = False
    return_dict = {"task": task_dict}
    return jsonify(return_dict), 200
#----------------------------------------------------------------------
# ---------------GOAL-----------------------------------------------
#----------------------------------------------------------------------
# This is the BluePrint object that helps to "connect" my functions to
# endpoints and HTTP methods for goals.
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def post_goal():
    # request.get_json() returns a dictionary with keys: "title"
    # Use corresponding values to create the Task instance.
    post_dict = request.get_json()
    print(post_dict)
    
    if 'title' not in post_dict:
        return make_response({"details":"Invalid data"},400)
    
    title = post_dict['title']
    goal = Goal(title=title)
    db.session.add(goal)
    db.session.commit()

    goal_dict={}
    goal_dict['id'] = goal.id
    goal_dict['title'] = goal.title
    return_dict = {"goal": goal_dict}
    return jsonify(return_dict), 201

#------------GET ALL GOALS---------------
@goals_bp.route("", methods=["GET"]) 
def get_all_goals():
    
    goal_db = Goal.query.all()

    
    goal_dict = {}
    goals_response = [] 
    for goal in goal_db:  
        goal_dict = {'id': goal.id,
                'title': goal.title
    }             
        goals_response.append(goal_dict)
    return jsonify(goals_response), 200  

#-----------------------------------
@goals_bp.route("/<id>",methods = ["GET"]) 
def get_goal_by_id(id):
    # Remember that id from the request is a string and not an integer

    goal = Goal.query.get(id)
    if (goal == None):
        abort(make_response({"message":f"goal {id} not found"}, 404))
    else:
        goal_dict={}
        goal_dict['id'] = goal.id
        goal_dict['title'] = goal.title
        return_dict = {"goal": goal_dict}
        return jsonify(return_dict), 200

#------------PUT Method - update goal by id---------
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal_by_id(id):
    goal = Goal.query.get(id)
    
    if (goal == None):
        abort(make_response({"message":f"goal {id} not found"}, 404))

    update_dict = request.get_json()
    if 'title' not in update_dict:
        return make_response({"details":"Invalid data"},400)

    title = update_dict['title']
    goal.title = title
    
    db.session.commit()

    goal_dict={}
    goal_dict['id'] = goal.id
    goal_dict['title'] = goal.title
    
    return_dict = {"goal": goal_dict}
    return jsonify(return_dict), 200
#------------remove goal by id------------
@goals_bp.route("/<id>", methods=["DELETE"])
def remove_goal_by_id(id):
    goal = Goal.query.get(id)
    
    if (goal == None):
        abort(make_response({"message":f"goal {id} not found"}, 404))
    
    db.session.delete(goal)
    db.session.commit()
    return make_response({"details":f"Goal {id} \"{goal.title}\" successfully deleted"},200)
#------------------------------------------------
#----------------WAVE 6-------------------------
#---------------------------------------------------

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def associate_tasks_with_goal(goal_id):
    goal = Goal.query.get(goal_id)
    task_ids_dict = request.get_json()
    task_ids = task_ids_dict['task_ids']
    for id in task_ids:
        task = Task.query.get(id)
        task.goal = goal
        db.session.commit()
    
    response_dict = {
        "id": int(goal_id),
        "task_ids": task_ids
    }
    return jsonify(response_dict), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_associated_with_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal == None:
        abort(make_response({"message":f"goal {goal_id} not found"}, 404))
    
    tasks = goal.tasks # list of all task instances associated with the goal_id
    task_dicts = []
    for task in tasks:
        if task.completed_at == None:
            is_complete = False
        else:
            is_complete = True
        task_dict = {
            "id": task.id,
            "goal_id": goal.id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete
        }
        task_dicts.append(task_dict)

    response_dict = {
        "id": goal.id,
        "title": goal.title,
        "tasks": task_dicts
    }
    return jsonify(response_dict), 200