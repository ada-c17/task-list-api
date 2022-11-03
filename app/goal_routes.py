from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response,request					
from app import db	
from datetime import datetime, date, time, timezone
import requests

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# Helper Function
def validate_goal(id):
    try:
        goal_id = int(id)
    except ValueError:
            abort(make_response(jsonify(dict(details=f"Invalid id {goal_id}")), 400))

  
    goal = Goal.query.get(id)
    if goal:
        return goal

    abort(make_response(jsonify(dict(details=f"No goal with id {goal_id} found")), 404))

# CREATE NEW TASK
@goals_bp.route("", methods=[ "POST"])						
def create_goal():	
    request_body = request.get_json()	

    if request_body == {}:

        response_body = {
        "details": "Invalid data"
        }, 400

        return response_body
						
   					
    new_goal = Goal(						
        title=request_body["title"])				
       

    db.session.add(new_goal)  
    db.session.commit() 

    response_body = { "goal":
    {   
    "id": new_goal.goal_id,       
    "title": new_goal.title   
    }
    }, 201
      
    return response_body


@goals_bp.route("/<goal_id>", methods=["GET"])
# return dictionary with "goal" as key and the value is a nested dictionary

def get_task_by_id(goal_id):
    goal = validate_goal(goal_id)

    if goal == None:
        return []
    response_body = { "goal":
        {   
        "id": goal.goal_id,       
        "title": goal.title,   					
        }
    }
       
    return response_body 

# GET  ALL ROUTE
@goals_bp.route("", methods=["GET"])						
def get_all_goals():    

    goals = Goal.query.all()

    if goals == None:
            return []
    else:
        response_body = []
        for goal in goals:	            					
            response_body.append({					
            "id": goal.goal_id,					
            "title": goal.title,										
            })	
        
        return jsonify(response_body)

# # Update ONE Goal
@goals_bp.route("/<goal_id>", methods=["PUT"])

def update_task_by_id(goal_id):

    goal = validate_goal(goal_id)
    request_body = request.get_json()
   
    goal.title = request_body["title"]   


    response_body = { "goal":
        {   
        "id": goal.goal_id,       
        "title": goal.title,   
        }
    }
 
    db.session.commit()

    return  response_body


@goals_bp.route("/<goal_id>", methods=["DELETE"])

def delete_goal_by_id(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response_body = {
         "details": 
         f"Goal {goal.goal_id} \ {goal.title} \" successfully deleted"
    }

    return response_body


# NESTED ROUTE CREATE BY GOAL AND TASK
    # CREATE A GOAL THATS LINKED TO A TASK
    # USE THE GOALS bp

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])

def post_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        linked_task = Task.query.get(task_id)
        linked_task.goal_id = goal_id

    db.session.commit()


    linked_task_ids = []
    for task in goal.tasks:
        linked_task_ids.append(task.task_id)

    return {"id":goal.goal_id, "task_ids":linked_task_ids}, 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_one_goal(goal_id):

    goal = validate_goal(goal_id)
    response = {
        "id": goal.goal_id,					
        "title": goal.title,
        "tasks": []
    }
    # tasks_response = []
    for task in goal.tasks:
        response["tasks"].append(				
      
         
                {
                "id": task.task_id,	
                "goal_id": goal.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": True if task.completed_at else False 
                }
            					
            )	        
    return jsonify(response)