from app.models.goal import Goal
from app import db
import json
from flask import Blueprint, request, jsonify, abort, make_response
from app.routes.tasks import tasks_bp, validate_task


goals_bp = Blueprint('goals_bp', __name__, url_prefix='/goals')


@goals_bp.route('', methods=['POST'])
def create_a_goal():
    request_body = request.get_json()

    try:
        goal = Goal(title=request_body['title'])
    
    except:
        return {'details': 'Invalid data'}, 400

    db.session.add(goal)
    db.session.commit()

    return {'goal': goal.to_dict()}, 201


@goals_bp.route('', methods=['GET'])
def get_all_goals():
    goals = Goal.query.all()
    
    goal_list = []
    for goal in goals:
        goal_list.append(goal.to_dict())

    return jsonify(goal_list), 200


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return jsonify({'details': f'Invalid goal id: {goal_id}. Goal id must be an integer'}), 400

    goal = Goal.query.get(goal_id)

    if goal is None:
        goal_not_found = {'details': f'Could not find goal id {goal_id}'}
        abort(make_response(jsonify(goal_not_found), 404))
        
    return goal


@goals_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    
    return {'goal': goal.to_dict()}, 200


@goals_bp.route('/<goal_id>', methods=['PUT'])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    try:
        goal.title = request_body['title']
    
    except KeyError:
        return jsonify({'details': 'Request must include title'}), 400

    db.session.commit()

    return {'goal': goal.to_dict()}, 200
        

@goals_bp.route('/<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({'details': f'Goal {goal_id} \"{goal.title}\" successfully deleted'}), 200


@goals_bp.route('/<goal_id>/tasks', methods=['POST'])
def assign_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    
    request_body = request.get_json()

    task_list = request_body["task_ids"]

    for task in task_list:
        valid_task = validate_task(task)
        goal.tasks.append(valid_task)
    db.session.commit()

    return jsonify({
        'id': goal.goal_id,
        'task_ids': task_list
    }), 200


@goals_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_tasks_for_goal(goal_id):
    goal = validate_goal(goal_id)

    task_list = []

    for task in goal.tasks:
        task_list.append(task.to_dict())

    return jsonify({
        'id': goal.goal_id,
        'title': goal.title,
        'tasks': task_list
    }), 200


