import json, os, requests
from urllib import response

from app import db
from app.models.task import Task
from app.models.goal import Goal

from datetime import datetime
from attr import validate
from sqlalchemy import true
from flask import Blueprint, jsonify, abort, make_response, request
from tests.conftest import one_task


# ------------------------ BLUEPRINT INSTANCES ------------------------ # 
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# Add goal Blueprint
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


# ------------------------ SLACK ------------------------ # 
SLACK_URL = "https://slack.com/api/chat.postMessage"
SLACK_TOKEN =  os.environ.get("SLACK_TOKEN")


# ------------------------ HELPER FUNCTIONS ------------------------ #

def validate_task(task_id):
    # Check if task_id is a valid integer
    try:
        task_id = int(task_id)
    except:
        # If it's not, 400 response code
        abort(make_response({"message" : f"Task {task_id} is invalid."}, 400))

    # Search for this task_id in the Task Blueprint
    task = Task.query.get(task_id)

    # If this specific task isn't found, 404 response code
    if not task:
        abort(make_response({"message" : f"This task is not found."}, 404))
    # If task found, return it 
    return task



def slack_notification(task_to_notify):
    headers = {"Authorization" : f"Bearer {SLACK_TOKEN}"}

    q_params = {
        "channel": "task-notifications", 
        "text": f"Someone just completed the task {task_to_notify.title}"
    }
    
    slack_request = requests.post(SLACK_URL, headers=headers, params=q_params)
    
    return slack_request



def format_response_body(task):

    if task.completed_at:
        is_complete = True
    else:
        is_complete = False
    
    response_body = jsonify({"task" : 
        {
            "id" : task.task_id,
            "title" : task.title,
            "description" : task.description,
            "is_complete" : is_complete
        }
    })

    return response_body



################# TASKS #################

# ------------------------ GET REQUESTS ------------------------ #

# ---- GET ALL TASKS ---- #
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    params = request.args

    all_tasks = Task.query.all()

    # Create the response body
    task_response = []
    
    for task in all_tasks:
        if task.completed_at == None:
            task_response.append(
                {
                    "id" : task.task_id,
                    "title" : task.title,
                    "description" : task.description,
                    "is_complete" : False
                }
            )
        else:
            task_response.append(
                {
                    "id" : task.task_id,
                    "title" : task.title,
                    "description" : task.description,
                    "is_complete" : True
                }
            )


    # Sorting Response body if there's a query parameter "sort"
    if "sort" in params:
        query_param = request.args.get("sort")

        if query_param == "asc":
            task_response = sorted(task_response, key=lambda a: a["title"])
        elif query_param == "desc":
            task_response = sorted(task_response, key=lambda d: d["title"], reverse=True)


    return jsonify(task_response)




# ---- GET ONE TASK BY ID ---- #
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):

    task = validate_task(task_id)

    return format_response_body(task), 200



# ------------------------ POST REQUESTS ------------------------ #

# ---- CREATE A TASK ---- #
@tasks_bp.route("", methods=["POST"])
def create_task():
    
    request_body = request.get_json()

    # Title or Description is not in request body, return 400 response
    if "title" not in request_body or "description" not in request_body:
        return jsonify({
            "details" : "Invalid data"
        }), 400



    if "completed_at" in request_body:

        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=datetime.utcnow())
    else:

        new_task = Task(title=request_body["title"],
                        description=request_body["description"])


    # Add new task and commit change
    db.session.add(new_task)
    db.session.commit()

    return format_response_body(new_task), 201



# ------------------------ PUT REQUESTS ------------------------ #

# ---- UPDATE A TASK ---- #
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task_to_update = validate_task(task_id)

    request_body = request.get_json()

    # If task id is valid, update Title and Description
    # Using the Title and Description in the request body
    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]


    # Commit the change and send response body
    db.session.commit()

    return format_response_body(task_to_update), 200



# ------------------------ PATCH REQUESTS ------------------------ #

# ---- INCOMPLETED TASK, MARK IT AS COMPLETE ---- #
# ---- ALSO COMPLETED TASK, MARK IT AS COMPLETE ---- #
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_as_complete(task_id):

    verified_task = validate_task(task_id)

    if verified_task:
        # Get the specific task to mark
        task_to_mark_complete = Task.query.get(task_id)

    # If task is incomplete (aka set to None), assign a datatime value to it
    if not task_to_mark_complete.completed_at:
        # Set completed_at as the datetime value
        task_to_mark_complete.completed_at = datetime.utcnow()

    # If task is already marked as 'complete' 
    # (aka has a datetime value), return the response body where 'is_complete' is True
    if task_to_mark_complete.completed_at:

        # Task is marked 'complete' so we want to have a notification on Slack
        slack_notification(task_to_mark_complete)

        
    # Add update, commit, and send response body 
    db.session.add(task_to_mark_complete)
    db.session.commit()
    # return response_body, 200

    return format_response_body(task_to_mark_complete), 200



# ---- COMPLETED TASK, MARK IT AS INCOMPLETE ---- #
# ---- ALSO INCOMPLETED TASK, MARK IT AS INCOMPLETE ---- #
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_as_incomplete(task_id):

    verified_task = validate_task(task_id)

    if verified_task:
        # Get the specific task to mark
        task_to_mark_incomplete = Task.query.get(task_id)

        # Task.completed_at is currently marked so set it to None
        if task_to_mark_incomplete.completed_at:
            task_to_mark_incomplete.completed_at = None
        

    # Add update, commit, and send response body 
    db.session.add(task_to_mark_incomplete)
    db.session.commit()

    return format_response_body(task_to_mark_incomplete), 200



# ------------------------ DELETE REQUESTS ------------------------ #

# ---- DELETE ONE TASK ---- #
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):

    verified_task = validate_task(task_id)

    # If task id is valid, get this specific task
    if verified_task:
        task_to_delete = Task.query.get(task_id)

    # Delete the task and commit the changes
    db.session.delete(task_to_delete)
    db.session.commit()

    return {
        "details": f'Task {task_id} \"{task_to_delete.title}\" successfully deleted'
    }, 200








################# GOALS #################

def format_goal_response_body(goal):

    response_body = jsonify({"goal" : 
        {
            "id" : goal.goal_id,
            "title" : goal.title,
        }
    })

    return response_body


def validate_goal(goal_id):
    # Check if task_id is a valid integer
    try:
        goal_id = int(goal_id)
    except:
        # If it's not, 400 response code
        abort(make_response({"message" : f"Goal ID is invalid."}, 400))


    validated_goal = Goal.query.get(goal_id)

    # If this specific goal isn't found, 404 response code
    if not validated_goal:
        abort(make_response({"message" : f"This goal is not found."}, 404))
    
    return validated_goal



# ------------------------ GET REQUESTS ------------------------ #

# ---- GET ALL GOALS ---- #
@goals_bp.route("", methods=["GET"])
def get_all_goals():

    all_goals = Goal.query.all()

    # Create the response body
    goal_response = []


    for goal in all_goals:

        goal_response.append(
            {
                "id" : goal.goal_id,
                "title" : f"{goal.title}"
            }
        )

    return jsonify(goal_response), 200



# ---- GET ONE GOAL BY ID ---- #
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):

    # Check if goal_id is a valid integer
    try:
        goal_id = int(goal_id)
    except:
        # If it's not, 400 response code
        abort(make_response({"message" : f"Goal ID is invalid."}, 400))

    # Search for this goal_id in the Goal Blueprint
    goal = Goal.query.get(goal_id)



    # If this specific goal isn't found, 404 response code
    if not goal:
        abort(make_response({"details" : f"Invalid data"}, 404))

    return format_goal_response_body(goal), 200




# ------------------------ POST OR PUT REQUESTS ------------------------ #


# ---- CREATE A GOAL ---- #

@goals_bp.route("", methods=["POST"])
def create_goal():

    request_body = request.get_json()

    if not request_body:
        abort(make_response({"details" : f"Invalid data"}, 400))


    new_goal = Goal(title=request_body["title"])

    # Add new task and commit change
    db.session.add(new_goal)
    db.session.commit()

    response_body = jsonify({ "goal" : 
        {
            "id" : new_goal.goal_id,
            "title" : new_goal.title
        }
    })

    return response_body, 201



# ---- UPDATE GOAL ---- #

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    goal_to_update = validate_goal(goal_id)

    request_body = request.get_json()


    if "title" not in request_body:
        return {
            "details" : "Invalid data"
        }, 400


    goal_to_update.title = request_body["title"]

    db.session.commit()

    return format_goal_response_body(goal_to_update), 200


# ---- DELETE GOAL ---- #
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):

    goal_to_delete = validate_goal(goal_id)


    db.session.delete(goal_to_delete)
    db.session.commit()

    return {
        "details" : f"Goal {goal_id} \"{goal_to_delete.title}\" successfully deleted"
    }, 200





################# NESTED ROUTES #################

# # ---- CREATE A GOAL ---- #

# @goals_bp.route("", methods=["POST"])
# def create_goal():

#     request_body = request.get_json()

#     if not request_body:
#         abort(make_response({"details" : f"Invalid data"}, 400))


#     new_goal = Goal(title=request_body["title"])

#     # Add new task and commit change
#     db.session.add(new_goal)
#     db.session.commit()

#     response_body = jsonify({ "goal" : 
#         {
#             "id" : new_goal.goal_id,
#             "title" : new_goal.title
#         }
#     })

#     return response_body, 201

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):

    # Get the goal to post the tasks to
    goal_for_post = validate_goal(goal_id)
    
    request_body = request.get_json()

    # Check that "task_ids" is in the request_body
    if "task_ids" in request_body:
        # task_ids = request_body["task_ids"]

        # Loop through the "task_ids"
        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal_for_post.goal_id


    db.session.commit()

    # Add to Goal's task_id's list
    response_body = {
        "id" : goal_for_post.goal_id, 
        "task_ids" : request_body["task_ids"]
    }

    return response_body, 200




@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_one_goal(goal_id):
    
    # Get one goal
    goal_to_get = validate_goal(goal_id)

    # goal_request_body = request.get_json()

    tasks_response = []


    if goal_to_get.tasks:

        for task in goal_to_get.tasks:

            if not task.completed_at:
                task.completed_at = False

            tasks_response.append(
                {
                "id" : task.task_id,
                "goal_id" : task.goal_id,
                "title" : task.title,
                "description": task.description,
                "is_complete": task.completed_at,
                }
            )

    # return tasks_response, 200

    response_body = {
        "id" : goal_to_get.goal_id, 
        "title" : goal_to_get.title,
        "tasks" : tasks_response
    }

    return response_body, 200
