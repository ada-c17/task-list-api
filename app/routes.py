from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db
from datetime import datetime
import requests
import os
from app.models.goal import Goal
from dotenv import load_dotenv


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix='/tasks')

goals_bp = Blueprint("goals_bp",  __name__, url_prefix='/goals')

load_dotenv()


# HELPER FUNCTIONS

def validate(id, type):
    try:
        id = int(id)
    except ValueError:
        response = {"msg":f"Invalid id: {id}"}
        abort(make_response(jsonify(response), 400))
    
    if type == "task":
        chosen = Task.query.get(id)
    else:
        chosen = Goal.query.get(id)

    if chosen is None:
        if type == "task":
            response =  {"msg": "Task not found"}
        else:
            response =  {"msg": "Goal not found"}

        abort(make_response(jsonify(response), 404))
    return chosen

#helper function, checks if TASK is complete
def check_if_completed(task):
    if task.completed_at is None:
        is_complete = False
    else:
        is_complete = True
    return is_complete

#helper function, makes TASK responses
def make_task_response(task):
    is_complete = check_if_completed(task)
    if task.goal_id is None:
        response = {
            "task": {
                'id': task.task_id,
                'title': task.title,
                'description': task.description,
                'is_complete': is_complete
            }
        }
    else:
        response = {
            "task": {
                'id': task.task_id,
                'goal_id': task.goal_id,
                'title': task.title,
                'description': task.description,
                'is_complete': is_complete
            }
        }
    return response
    
#helper function, makes GOAL responses
def make_goal_response(goal):
    response = {
        "goal":{
            "id": goal.goal_id,
            "title": goal.title
            }
        }
    return response


#helper function, sorts tasks by title
def sort_tasks(params, tasks_response):
    sort_type = None
    if params["sort"] == "asc":
        #ascending
        sort_type = "A"
    else:
        #descending
        sort_type = "D"

    if sort_type == "A":
        tasks_response = (sorted(tasks_response, key=lambda task: task['title']))

    elif sort_type == "D":
        tasks_response = (sorted(tasks_response, key=lambda task: task['title'], reverse = True))

    return tasks_response


# TASKS

@tasks_bp.route('', methods = ['POST'])
def create_one_task():
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        response = {"details": "Invalid data"}
        abort(make_response(jsonify(response), 400))

    if "completed_at" in request_body:
        new_task = Task(title=request_body['title'], 
                    description=request_body['description'], completed_at=request_body['completed_at'])
    else:
        new_task = Task(title=request_body['title'], 
                    description=request_body['description'])

    db.session.add(new_task)
    db.session.commit()
    response = make_task_response(new_task)
    return jsonify(response), 201


@tasks_bp.route('/<task_id>', methods = ['GET'])
def get_one_task(task_id):
    chosen_task = validate(task_id, "task")
    response = make_task_response(chosen_task)
    return jsonify(response), 200


@tasks_bp.route('', methods = ['GET'])
def get_all_tasks():

    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        is_complete = check_if_completed(task)
        if task.goal_id is None:
            tasks_response.append({
            'id': task.task_id,
            'title': task.title,
            'description': task.description,
            'is_complete': is_complete
        })

        else:
            tasks_response.append({
                'id': task.task_id,
                'goal_id': task.goal_id,
                'title': task.title,
                'description': task.description,
                'is_complete': is_complete
            })

    #check params for sorting
    params = request.args
    if "sort" in params:
        tasks_response = sort_tasks(params, tasks_response)

    return jsonify(tasks_response)




#SLACK API  - sends message to slack
def message_slack(task):
    SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
    PATH = 'https://slack.com/api/chat.postMessage'
    query_params = {
        "channel":"task-notifications",
        "text":f"Someone just completed the task {task.title}"
    }
    header = {"Authorization" : f"Bearer {SLACK_TOKEN}"}

    response = requests.post(PATH, params=query_params, headers=header)
    return response


@tasks_bp.route('/<task_id>/mark_complete', methods = ['PATCH'])
def mark_complete(task_id):
    chosen_task = validate(task_id, "task")

    #check if task was already completed, if not, send message to slack
    if not check_if_completed(chosen_task):
        message_slack(chosen_task)

    chosen_task.completed_at = datetime.utcnow()
    db.session.commit()
    response = make_task_response(chosen_task)
    return jsonify(response), 200


@tasks_bp.route('/<task_id>/mark_incomplete', methods = ['PATCH'])
def mark_incomplete(task_id):
    chosen_task = validate(task_id, "task")
    chosen_task.completed_at = None
    db.session.commit()
    response = make_task_response(chosen_task)
    return jsonify(response), 200


@tasks_bp.route('/<task_id>', methods = ['PUT'])
def update_task(task_id):
    chosen_task = validate(task_id, "task")

    request_body = request.get_json()
    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
    except KeyError:
        return{
            "msg": "title and description are required"
        }, 400
    
    db.session.commit()
    response = make_task_response(chosen_task)
    return jsonify(response), 200

@tasks_bp.route('/<task_id>', methods = ['DELETE'])
def delete_task(task_id):

    chosen_task = validate(task_id, "task")

    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f"Task {chosen_task.task_id} \"{chosen_task.title}\" successfully deleted"
    }, 200



# GOALS

@goals_bp.route('', methods = ['POST'])
def create_one_goal():

    request_body = request.get_json()

    if "title" not in request_body:
        response = {"details": "Invalid data"}
        abort(make_response(jsonify(response), 400))

    new_goal = Goal(title=request_body['title'])

    db.session.add(new_goal)
    db.session.commit()
    response = make_goal_response(new_goal)
    return jsonify(response), 201


@goals_bp.route('/<goal_id>', methods = ['GET'])
def get_one_goal(goal_id):
    chosen_goal = validate(goal_id, "goal")

    response = make_goal_response(chosen_goal)
    return jsonify(response), 200



@goals_bp.route('', methods = ['GET'])
def get_all_goals():

    goals = Goal.query.all()
    goals_response = []
    for goal in goals:

        goals_response.append({
            'id': goal.goal_id,
            'title': goal.title,
        })

    return jsonify(goals_response)


@goals_bp.route('/<goal_id>', methods = ['PUT'])
def update_goal(goal_id):

    chosen_goal = validate(goal_id, "goal")
    request_body = request.get_json()
    try:
        chosen_goal.title = request_body["title"]
    except KeyError:
        return{
            "msg": "title is required"
        }, 400
    
    db.session.commit()

    response = make_goal_response(chosen_goal)
    return jsonify(response), 200



@goals_bp.route('/<goal_id>', methods = ['DELETE'])
def delete_goal(goal_id):

    chosen_goal = validate(goal_id, "goal")

    db.session.delete(chosen_goal)
    db.session.commit()

    return {
        "details": f"Goal {chosen_goal.goal_id} \"{chosen_goal.title}\" successfully deleted"
    }, 200


# NESTED ROUTES

@goals_bp.route('/<goal_id>/tasks', methods = ['POST'])
def send_tasks_to_goal(goal_id):
    chosen_goal = validate(goal_id, "goal")

    request_body = request.get_json()

    for task in request_body["task_ids"]:
        chosen_task = validate(task, "task")
        chosen_task.goal_id = chosen_goal.goal_id

    db.session.commit()
    response = {
        "id": chosen_goal.goal_id,
        "task_ids":request_body["task_ids"]
    }

    return jsonify(response), 200


@goals_bp.route('/<goal_id>/tasks', methods = ['GET'])
def get_tasks_of_one_goal(goal_id):

    chosen_goal = validate(goal_id, "goal")

    tasks = []
    for task in chosen_goal.tasks:
        is_complete = check_if_completed(task)
        tasks.append(
            {
                "id":task.task_id,
                "goal_id":chosen_goal.goal_id,
                "title":task.title,
                "description":task.description,
                "is_complete":is_complete
            }
        )
    response = {
        "id":chosen_goal.goal_id,
        "title":chosen_goal.title,
        "tasks":tasks
    }

    return jsonify(response)

