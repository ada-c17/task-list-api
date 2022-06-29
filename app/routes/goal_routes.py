from pydoc import describe
from urllib import response
from flask import Blueprint, jsonify, request, make_response,abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from .helper import goal_validate_client_requests, validate_goal, validate_task

goals_bp = Blueprint("goals", __name__,url_prefix="/goals" )

#GET all
@goals_bp.route("", methods = ["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())
    
    return jsonify(goals_response),200


#GET one
@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    
    return {"goal": goal.to_json()},200


#CREATE one
@goals_bp.route("", methods = ["POST"])
def create_one_goal():
    
    request_body = request.get_json()
    if "title" in request_body:
    # new_goal = goal_validate_client_requests(request_body)

    #?????? why below does not work
    # new_goal = Goal(title = request_body["title"])
        new_goal = Goal.create_goal(request_body)
        db.session.add(new_goal)
        db.session.commit()
    
        return {"goal": new_goal.to_json()}, 201   
    else:
        return  {"details": "Invalid data"}, 400
        

    


#UPDATE one goal 
@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_one_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_json()}), 200)


#DELETE 
@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200



# Sending a List of Task IDs to a Goal
@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def create_tasks(goal_id):
#1 get goal for adding tasks:
    goal = validate_goal(goal_id)

#2 get tasks that need to add to goal
    #  2.a get task ids from client
    request_body = request.get_json()
    #  2.b get tasks by ids from DB and connect with FK
    for id in request_body["task_ids"]:
        task = validate_task(id)
        task.goal_id = goal_id
        # or   -  add a list of tasks to goal
        # goal.tasks.append(task)
        # or   -  assign goal to task.goal
        # task.goal = goal

    db.session.commit()

#3 create respons body and return it
    tasks_id_list =[]
    for task in goal.tasks:
        tasks_id_list.append(task.id)
    response_body = {
        "id": goal.goal_id,
        "task_ids": tasks_id_list
    }
    return make_response(jsonify(response_body), 200)


#GET task from specific goal
@goals_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_task_from_specific_goal(goal_id):
    #get target goal
    goal = validate_goal(goal_id)
    
    
    tasks_list = []
    for task in goal.tasks:
        tasks_list.append( task.to_json())

    response_boday = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_list
    }


    return response_boday, 200

#Get a specific Task under given Goal
@goals_bp.route("/tasks/<id>", methods = ["GET"])
def get_task_under_specific_goal(id):
    task = validate_task(id)
    goal_id = task.goal_id

    response_body = task.to_json()
    return response_body, 200
