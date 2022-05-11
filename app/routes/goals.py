from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db

goals_bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({'details': 'Invalid data'}, 400))
    
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({'details': f'No goal with id {goal_id}'}, 404))

    return goal


@goals_bp.route('', methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body['title'])
    except KeyError:
        return {"details": "Invalid data"}, 400
    db.session.add(new_goal)
    db.session.commit()

    rsp = {'goal': {
        'id': new_goal.id,
        'title': new_goal.title
        }}
    
    return jsonify(rsp), 201


@goals_bp.route('', methods=['GET'])
def get_all_goals():
    response_body = []
    goals = Goal.query.all()

    for goal in goals:
        response_body.append({
            'id': goal.id,
            'title': goal.title
        })
    
    return jsonify(response_body), 200


@goals_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_goal_id(goal_id)
    rsp = {'goal': {
        'id': goal.id,
        'title': goal.title
        }}

    return jsonify(rsp), 200


@goals_bp.route('/<goal_id>', methods=['PUT'])
def update_one_goal(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()

    try:
        goal.title = request_body['title']
    except KeyError:
        return {"details": "Invalid data"}, 400
        
    db.session.commit()

    rsp = {'goal': {
        'id': goal.id,
        'title': goal.title
        }}
    return jsonify(rsp), 200


@goals_bp.route('/<goal_id>', methods=['DELETE'])
def delete_one_goal(goal_id):
    goal = validate_goal_id(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"}), 200


@goals_bp.route('/<goal_id>, tasks', methods=['GET'])
def get_tasks_list(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()

    for id in request_body['task_ids']:
        goal.tasks.append(id)
    
    rsp = {
        'id': goal.id,
        'task_id': goal.tasks
    }
    return jsonify(rsp), 200
