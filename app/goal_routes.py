from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.validate_helper import validate_element
from flask import Blueprint, request, make_response, jsonify

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


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


#POST one goal by id
@goals_bp.route("", methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    new_goal = Goal.create_task(request_body)
    
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_json()}), 201


#UPDATE one goal by id
@goals_bp.route("<goal_id>", methods=['PUT'])
def update_one_goal(goal_id):
    goal = validate_element(goal_id, "goal")
    request_body = request.get_json()

    goal.title = request_body['title']

    db.session.commit()
    
    return make_response(jsonify({"goal" : goal.to_json()}), 200)


#DELETE one goal by id
@goals_bp.route('<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_element(goal_id, "goal")

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}), 200)


# ----------------------------- Getting Tasks for Individual Goals ---------------------------------------

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
        task.goal_id = goal.id
        task_list.append(task)


    goal.tasks = task_list
    db.session.commit()

    return make_response(jsonify({
        "id" : goal.id,
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
        "id": goal.id,
        "title": goal.title,
        "tasks": task_list
    }), 200)
