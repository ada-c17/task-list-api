
from wsgiref.util import request_uri
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import asc
from datetime import datetime
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_element(element_id, element):
    try:
        element_id = int(element_id)
    except:
        return abort(make_response({"details": "Invalid data"}, 400))
    if element == "task":
        element = Task.query.get(element_id)
        name = "Task"
    elif element == "goal":
        element = Goal.query.get(element_id)
        name = "Goal"
    if not element:
        return abort(make_response({"message" : f"{name} {element_id} is not found"}, 404))
    return element


    ########TASK ROUTES###########

#GET all tasks
@tasks_bp.route("", methods=["GET"])
def get_all_task():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    
    return make_response(jsonify(tasks_response), 200)

    #GET one task
@tasks_bp.route("<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = validate_element(task_id, "task")
    return jsonify({"task": task.to_json()}), 200
    
#POST a new task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.create_task(request_body)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task": new_task.to_json()}), 201

    #UPDATE a task
@tasks_bp.route("<task_id>", methods=['PUT'])
def update_one_task(task_id):
    task = validate_element(task_id, "task")
    request_body = request.get_json()
    task.title = request_body['title']
    task.description = request_body['description']
    db.session.commit()
    return make_response(jsonify({"task" : task.to_json()}), 200)

    #DELETE a task
@tasks_bp.route('<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = validate_element(task_id, "task")
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"details": 'Task 1 Go on my daily walk successfully deleted'} ), 200)
    
#MARK task complete
@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_task_complete(task_id):
    task = validate_element(task_id, "task")
    task.completed_at = datetime.now()
    db.session.commit()
    slack_api_url = "https://slack.com/api/chat.postMessage"
    params = {
        "channel" : "task-notifications",
        "text" : f"Someone just completed the task {task.title}"
    }
    headers = {
        "Authorization" : f"Bearer {os.environ.get('SLACK_API_HEADER')}"
    }
    requests.get(url=slack_api_url, params=params, headers=headers)
    
    return make_response(jsonify({"task" : task.to_json()}))

    #MARK task incomplete
@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_task_incomplete(task_id):
    task = validate_element(task_id, "task")
    task.completed_at = None
    db.session.commit()
    return make_response(jsonify({"task" : task.to_json()})) 





######## GOAL ROUTES ########## 

#GET all goals
@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())
    return make_response(jsonify(goals_response), 200)

#GET one goal by id
@goals_bp.route("<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_element(goal_id, "goal")
    return jsonify({"goal": goal.to_json()}), 200

#POST new goal
@goals_bp.route("", methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    new_goal = Goal.create_task(request_body)
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"goal": new_goal.to_json()}), 201

#UPDATE goal by id
@goals_bp.route("<goal_id>", methods=['PUT'])
def update_one_goal(goal_id):
    goal = validate_element(goal_id, "goal")
    request_body = request.get_json()
    goal.title = request_body['title']
    db.session.commit()
    return make_response(jsonify({"goal" : goal.to_json()}), 200)

##DELETE a goal
@goals_bp.route('<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_element(goal_id, "goal")
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}), 200) 


    ###### Goals via ONE id######

#POST - attach tasks onto one goal
@goals_bp.route('/<goal_id>/tasks', methods=['POST'])
def create_task_for_goal(goal_id):
    goal = validate_element(goal_id, "goal")
    request_body = request.get_json()
    task_list = []
    task_ids = request_body["task_ids"]
    print(task_ids)
    for task_id in task_ids:
        task = validate_element(task_id, "task")
        task.goal_id = goal.goal_id
        task_list.append(task)

    goal.tasks = task_list
    db.session.commit()
    return make_response(jsonify({
        "id" : goal.goal_id,
        "task_ids" : task_ids
    }), 200)

#Get all tasks for one goal
@goals_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_task_for_goal(goal_id):
    goal = validate_element(goal_id, "goal")
    tasks = Task.query.filter_by(goal=goal)
    task_list = []

    for task in tasks:
        task_list.append(task.to_json())
    return make_response(jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_list
    }), 200)



# def error_message(message, status_code):
#     abort(make_response({"message":message}, status_code))


# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort (make_response(f"Task {task_id} invalid", 400))

#     task = Task.query.get(task_id)
#     if not task:
#         abort (make_response({"message" : f"Task given is invalid"}, 404))

#     return task

# def validate_request(request):
#     request_body = request.get_json()
#     try:
#         request_body["title"]
#         request_body["description"]
#     except KeyError:
#         abort (make_response({"details" : f"Invalid data"}, 404))  
#     return request_body      
# # VALIDATE ID
# def validate_id(task_id):
#     try:
#         task_id = int(task_id)
#     except ValueError:
#         abort(make_response(jsonify(f"Task {task_id} is invalid"), 400))
#     task = Task.query.get(task_id)
#     if not task:
#         abort(make_response(jsonify(f"Task {task_id} not found"), 404))
#     return task


# #POST

# @tasks_bp.route("", methods=["POST"])
# def create_new_task():
#     request_body = request.get_json()
#     request_body = validate_request(request)
#     new_task = Task(
#         title=request_body["title"],
#         description= request_body["description"],
#         completed_at= request_body["completed_at"] if "completed_at" in request_body else None
#     )        
    
#     # if :
#     #         completion_time = request_body["completed_at"]
#     #         new_task = Task(
#     #             title=request_body["title"],
#     #             description=request_body["description"],
#     #             completed_at = completion_time
#     #         )
#     # except KeyError:
#     #         new_task = Task(
#     #             title=request_body["title"],
#     #             description=request_body["description"]
#     #         )
#     db.session.add(new_task)
#     db.session.commit()

#     return make_response(jsonify({"message" : f"Task was successfully created"}, 201))

# #GET

# @tasks_bp.route("", methods=("GET",))
# def read_all_books():
#     #get query from url
#     title_param = request.args.get("title")
#     description_param = request.args.get("description")
#     is_complete_param =request.args.get("is_complete")
#     sort_param = request.args.get("sort")

#     #Initialize
#     tasks = Task.query

#     #search
#     if title_param:
#         tasks = tasks.filter_by(name=title_param)
#         tasks = tasks.filter_by(title=title_param)
#     if description_param:
#         tasks = tasks.filter_by(description=description_param)
#     if is_complete_param:
#         tasks = tasks.filter_by(color=is_complete_param)
#     if sort_param == "asc":
#         tasks = tasks.order_by(Task.title.asc())
#     elif sort_param == "desc":
#         tasks = tasks.order_by(Task.title.desc())
#     # execute the search and return all records that meet the criterium
#     tasks = tasks.all()
#     tasks_response = []
#     for task in tasks:
#         tasks_response.append(task.to_dict())
#     return jsonify(tasks_response)


# @tasks_bp.route("/<task_id>", methods=["GET"])
# def index_single_task(task_id):
#     task = validate_task(task_id)
#     return  make_response(jsonify({"task": task.to_dict()}), 200)


# @tasks_bp.route("/<task_id>", methods=["GET"])
# def read_one_task(task_id):
#     task = validate_task(task_id)
#     return task.to_dict()

# #PUT

# @tasks_bp.route("/<task_id>", methods=["PUT"])
# def update_task(task_id):
#     task = validate_task(task_id)
#     request_body = request.get_json()
#     task.title = request_body["title"]
#     task.description = request_body["description"]
#     task.completed_at = request_body["completed_at"]
#     db.session.commit()
#     return make_response(jsonify(f"Task #{task.id} successfully updated"))

# #DELETE
# @tasks_bp.route("/<task_id>", methods=["DELETE"])
# def delete_task(task_id):
#     task = validate_task(task_id)

#     db.session.delete(task)
#     db.session.commit()
#     return make_response(jsonify(f"Task #{task.id} successfully deleted"))    
#     # {'completed_at': None, 'description': 'Notice something new every day', 'is_complete': False, 'task_id': 1, 'title': 'Go on my daily walk #x1F3DE'} !=
#     # {'id': 1, 'title': 'Go on my daily walk #x1F3DE', 'description': 'Notice something new every day', 'is_complete': False}


# # MARK COMPLETE
# @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_complete(task_id):
#     task = validate_id(task_id)
#     task.completed_at = date.today()
#     db.session.commit()
#     return make_response({"task": task.to_dict()})

# # MARK INCOMPLETE
# @tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(task_id):
#     task = validate_id(task_id)
#     task.completed_at = None
#     db.session.commit()
#     return make_response({"task": task.to_dict()}) 
# #PATCH



# # def index_all_tasks():
# #     tasks = Task.query.all()
# #     result_list = [task.to_dict() for task in tasks]

# #     return make_response(jsonify(result_list), 200)
