
from flask import Blueprint,jsonify, request, make_response, abort
from app.models.goal import Goal
from app.models.task import Task
from app import db
from app.routes.task import validate_task



goal_bp = Blueprint("goals", __name__, url_prefix = "/goals")


#creating goal with post methods
@goal_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body :
        return jsonify({"details": "Invalid data"}), 400
    
    new_goal = Goal(title= request_body["title"])      
    db.session.add(new_goal)
    db.session.commit()
    return make_response(jsonify({"goal":new_goal.to_dict_goal()})), 201


#get all goals using GET methods
@goal_bp.route("", methods = ["GET"])
def get_all_goals():
    goals = Goal.query.all()
    return jsonify([goal.to_dict_goal() for goal in goals]), 200


#get one goal using GET methods and accessing with <goal_id>
@goal_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return jsonify({"goal":goal.to_dict_goal()}), 200


#updating goal info using PUT methods and accessing with <goal_id>
@goal_bp.route("/<goal_id>", methods = ["PUT"])
def replace_one_goal(goal_id):
    request_body = request.get_json()
    goal = validate_goal(goal_id)
    goal.title = request_body["title"] 
    db.session.commit()
    return jsonify({"goal":goal.to_dict_goal()}), 200


#removing one goal using DELETE methods and accessing with <goal_id>
@goal_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)
    db.session.delete(chosen_goal)
    db.session.commit()
    response_body = {"details": f"Goal {goal_id} \"Build a habit of going outside daily\" successfully deleted"}
    return jsonify(response_body), 200


#adding AND geting list of tasks 
@goal_bp.route("/<goal_id>/tasks", methods = ["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    try:
        task_ids = request_body["task_ids"]
    except KeyError:
        return jsonify({'msg': "Missing task_ids in request body"}), 400
    
    if not isinstance(task_ids, list):
        return jsonify({'msg': "Expected list of task ids"}), 400
    tasks = []
    for id in task_ids:
        task = Task.query.get(id)
        tasks.append(validate_task(id))
        
    for task in tasks:
        task.goal_id = goal_id

    db.session.commit()
    return jsonify({"id": goal.goal_id,"task_ids": task_ids}), 200


#get goal tasks using <goal_id>/tasks
@goal_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_goal_tasks(goal_id):
    chosen_goal = validate_goal(goal_id)
    tasks_list =[]
    for task in chosen_goal.tasks:
        tasks_list.append({
                "id":task.task_id,
                "goal_id":task.goal_id,
                'title':task.title,
                'description':task.description,
                'is_complete':bool(task.completed_at)})
        
    response= {
        "id":chosen_goal.goal_id,
        "title":chosen_goal.title,
        "tasks": tasks_list
    }
    return jsonify(response), 200


#validateing goal and using as a helper function 
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))
    chosen_goal = Goal.query.get(goal_id)
    if not chosen_goal:
        abort(make_response(jsonify({'details': f"Could not find goal"}), 404))  
    return chosen_goal
