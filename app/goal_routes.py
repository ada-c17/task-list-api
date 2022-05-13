from app import db
from app import helper_functions
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    '''
    POST method to /goals endpoint
    Input: title
    Returns: json response body with all input including id  
    '''
    request_body = request.get_json()
    if "title" not in request_body:
        return {
                "details": "Invalid data"
        }, 400
    else:
        new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_json()}), 201)

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    '''
    GET method to /goals endpoint
    Returns: json response body with id and title from all goals in /goals endpoints 
    '''
    goals = Goal.query.all()
    goals_response = [goal.to_json() for goal in goals]

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    '''
    GET method to /goals/<goal_id> endpoint
    Returns: json response body with id and title from goal with matching goal_id 
    '''
    goal = helper_functions.validate_goal(goal_id)
    goal = Goal.query.get(goal_id)

    return make_response(jsonify({"goal": goal.to_json()}))

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    '''
    PUT method to /goals/<goal_id> endpoint
    Input: title that needs to be updated
    Returns: json response body with all input, including id, from goal with matching id
    '''
    goal = helper_functions.validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_json()}))

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    '''
    DELETE method to /goals/<goal_id> endpoint
    Input: sending a goal with a specific id will delete the goal
    Returns: success message with specific goal id and goal title 
    '''
    goal = helper_functions.validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = (f'Goal {goal.goal_id} "{goal.title}" successfully deleted')

    return make_response(jsonify({"details": response})) 

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    '''
    POST method to /goals/<goal_id>/tasks endpoint
    Input: Specific goal with goal_id and a list of tasks that belong to the goal 
    Returns: json response body with goal_id and list of task_ids  
    '''
    goal = helper_functions.validate_goal(goal_id)
    request_body = request.get_json()

    for task in request_body["task_ids"]:
        task = helper_functions.validate_task(task)
        goal.tasks.append(task)
    
    db.session.commit()

    response = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }
    return make_response(jsonify(response), 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks_for_one_goal(goal_id): 
    '''
    GET method to /goals/<goal_id>/tasks endpoint
    Input: Specific goal with goal_id and a title of goal
    Returns: json response body with goal_id, title of goal, and a list of tasks with their ids, the coresponding
    goal_id, the tasks title, the task description, and is_complete (which evaluates to True or False)  
    '''
    goal = helper_functions.validate_goal(goal_id)
    
    response = {
        "id": goal.goal_id, 
        "title": goal.title, 
        "tasks": []
    }
    for task in goal.tasks: 
        response["tasks"].append(task.to_json())
    return response
    



