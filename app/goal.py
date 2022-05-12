import json, os, requests
from urllib import response

from app import db
from app.models.task import Task
from app.models.goal import Goal

from datetime import datetime
from attr import validate
from sqlalchemy import true
from flask import Blueprint, jsonify, abort, make_response, request
from app.task import validate_task
from tests.conftest import one_task


# ------------------------ BLUEPRINT INSTANCE ------------------------ # 
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")



# ------------------------ HELPER FUNCTIONS ------------------------ #

def format_goal_response_body(goal):

    response_body = jsonify({"goal" : 
        {
            "id" : goal.goal_id,
            "title" : goal.title,
        }
    })

    return response_body



def validate_goal(goal_id):
    # Check if goal_id is a valid integer
    try:
        goal_id = int(goal_id)
    except:
        # If it's not, return 400 response code
        abort(make_response({"message" : f"Goal ID is invalid."}, 400))


    validated_goal = Goal.query.get(goal_id)

    # If goal isn't found, return 404 response code
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
        # If it's not, return 400 response code
        abort(make_response({"message" : f"Goal ID is invalid."}, 400))

    # Search for this goal_id in the Goal Blueprint
    goal = Goal.query.get(goal_id)


    # If this goal isn't found, return 404 response code
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

    # Add new goal and commit change
    db.session.add(new_goal)
    db.session.commit()

    return format_goal_response_body(new_goal), 201



# ---- UPDATE GOAL ---- #

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    goal_to_update = validate_goal(goal_id)

    request_body = request.get_json()


    if "title" not in request_body:
        return {
            "details" : "Invalid data"
        }, 400

    # Update change to Goal Title
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

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):

    # Get the goal to post the tasks to
    goal_for_post = validate_goal(goal_id)
    
    # Getting the request body 
    request_body = request.get_json()

    # Verifying that the request body has a list of task ids
    try:
        task_ids = request_body["task_ids"]
    except KeyError:
        # Missing Task id in request body
        return jsonify(make_response({"message" : f"Missing list of task ids in request body."}, 400))

    if not isinstance(task_ids, list):
        return jsonify({"message" : f"Expected a list of task ids."}), 400



    task_id_list = []

    for id in task_ids:
        task_id_list.append(validate_task(id).task_id)
    
    for task_id in task_id_list:
        task_id.goal_for_post = goal_for_post


    

    # Check that "task_ids" is in the request_body
    if "task_ids" in request_body:

        # Loop through the "task_ids" and assign the Task foreign key to match the Goal primary key
        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal_for_post.goal_id
            db.session.add(task)
    else:
        # Check if "task_id" doesn't exist -->  404 
        abort(make_response({"message" : f"Sorry, task ids not found."}, 404))

    db.session.commit()

    # Add to Goal's task_id's list
    response_body = {
        "id" : goal_for_post.goal_id, 
        "task_ids" : task_id_list
    }

    return response_body, 200



@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_one_goal(goal_id):
    
    # Get one goal
    goal_to_get = validate_goal(goal_id)

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
    
    # If there are no tasks for the goal, an empty list will be returned (Test 4, Wave 6)


    response_body = {
        "id" : goal_to_get.goal_id, 
        "title" : goal_to_get.title,
        "tasks" : tasks_response
    }

    return response_body, 200