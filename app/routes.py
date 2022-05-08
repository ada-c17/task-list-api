import json
import os
from datetime import datetime
from attr import validate
from sqlalchemy import true
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from tests.conftest import one_task


# ---- CREATING BLUEPRINT INSTANCE---- # 
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


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

    return jsonify({"task" : 
        {
            "id" : task.task_id,
            "title" : task.title,
            "description" : task.description,
            "is_complete" : False
        }
    })



# ------------------------ POST REQUESTS ------------------------ #

# ---- CREATE A TASK ---- #
@tasks_bp.route("", methods=["POST"])
def create_task():
    
    request_body = request.get_json()

    # Title or Description is not in request body, return 400 response
    if not "title" in request_body or not "description" in request_body:
        return jsonify({
            "details" : "Invalid data"
        }), 400



    if "completed_at" in request_body:
        is_complete = True

        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=datetime.utcnow())
    else:
        is_complete = False

        new_task = Task(title=request_body["title"],
                        description=request_body["description"])


    # Add new task and commit change
    db.session.add(new_task)
    db.session.commit()

    response_body = jsonify({"task" : 
        {
            "id" : new_task.task_id,
            "title" : new_task.title,
            "description" : new_task.description,
            "is_complete" : is_complete
        }
    })

    return response_body, 201



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


    if "completed_at" in request_body:
        is_complete = True
    else:
        is_complete = False

    # Commit the change and send response body
    db.session.commit()

    response_body = jsonify({"task" : 
        {
            "id" : task_to_update.task_id,
            "title" : task_to_update.title,
            "description" : task_to_update.description,
            "is_complete" : is_complete
        }
    })

    return response_body, 200



# ------------------------ PATCH REQUESTS ------------------------ #

# ---- INCOMPLETED TASK, MARK IT AS COMPLETE ---- #
# ---- ALSO INCOMPLETED TASK, MARK IT AS COMPLETE ---- #
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_as_complete(task_id):

    verified_task = validate_task(task_id)

    if verified_task:
        # Get the specific task to mark
        task_to_mark_complete = Task.query.get(task_id)

        # If task is incomplete (aka set to None), assign a datatime value to it
        if task_to_mark_complete.completed_at == None:
            # Set completed_at as the datetime value
            task_to_mark_complete.completed_at = datetime.utcnow()

    # If task is already marked as 'complete' 
    # (aka datetime value), return the response body where 'is_complete' is True
    if task_to_mark_complete.completed_at:
        # If it's marked, set is_complete to True
        response_body = jsonify({"task" : 
            {
                "id" : task_to_mark_complete.task_id,
                "title" : task_to_mark_complete.title,
                "description" : task_to_mark_complete.description,
                "is_complete" : True
            }
        })
        
    # Add update, commit, and send response body 
    db.session.add(task_to_mark_complete)
    db.session.commit()
    return response_body, 200



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
        
    # If task is already marked as 'incomplete' 
    # (aka Null or None), return the response body where 'is_complete'is False
    if not task_to_mark_incomplete.completed_at:
        response_body = jsonify({"task" : 
            {
                "id" : task_to_mark_incomplete.task_id,
                "title" : task_to_mark_incomplete.title,
                "description" : task_to_mark_incomplete.description,
                "is_complete" : False
            }
        })

    # Add update, commit, and send response body 
    db.session.add(task_to_mark_incomplete)
    db.session.commit()
    return response_body, 200



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