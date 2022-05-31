from typing import Literal
from flask import Blueprint, Response, jsonify, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.commons import validate_and_get_by_id, get_filtered_and_sorted

QueryParam = str  # for type annotations


###############
# Goal routes #
###############

goal_bp = Blueprint('goals', __name__, url_prefix = '/goals')

@goal_bp.route('', methods = ['GET'])
def get_all_goals() -> tuple[Response, Literal[200]]:
    '''Queries DB for Goals and returns result as JSON data.'''

    if not request.args:
        return jsonify(Goal.query.all()), 200
    return jsonify(get_filtered_and_sorted(Goal, request.args)), 200

@goal_bp.route('', methods = ['POST'])
def create_goal() -> tuple[Response, Literal[201]]:
    '''Passes request JSON data to Goal.create() and saves result to DB.
    
    Returns details of created Goal instance as JSON data.
    '''

    new_goal = Goal.create(request.get_json())
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({'goal': new_goal}), 201

@goal_bp.route('/<goal_id>', methods = ['GET'])
def get_goal_by_id(goal_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Queries DB for specified Goal and returns basic info as JSON data.'''

    return jsonify({'goal': validate_and_get_by_id(Goal, goal_id)}), 200

@goal_bp.route('/<goal_id>', methods = ['PUT'])
def update_goal(goal_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Passes request JSON data to Goal.update() and saves result to DB.
    
    Returns details of updated Goal instance as JSON data.
    '''

    goal = validate_and_get_by_id(Goal, goal_id)
    goal.update(request.get_json())
    db.session.commit()

    return jsonify({'goal': goal}), 200

@goal_bp.route('/<goal_id>', methods = ['DELETE'])
def delete_goal(goal_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Queries DB for specified Goal instance and deletes it if found.'''

    goal = validate_and_get_by_id(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return jsonify({'details': (f'Goal {goal_id} "{goal.title}" '
                                f'successfully deleted')}), 200


###################################################
# Nested routes - Task actions accessed via goals #
###################################################

@goal_bp.route('/<goal_id>/tasks', methods = ['POST'])
def assign_tasks_to_goal(goal_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Assigns one or more Tasks to the specified Goal.
    
    A list of Task IDs is expected as JSON data in the request body. If any
    ID value is invalid, or if not all specified Tasks can be found, no changes
    are saved.
    '''

    goal = validate_and_get_by_id(Goal, goal_id)
    task_ids = request.get_json()['task_ids']
    
    for task_id in task_ids:
        task = validate_and_get_by_id(Task, task_id, errmsg=' No changes were made.')
        goal.tasks.append(task)
    db.session.commit()
    
    return jsonify({'id': int(goal_id), 'task_ids': [task.task_id for task in goal.tasks]}), 200

@goal_bp.route('/<goal_id>/tasks', methods = ['GET'])
def get_all_tasks_of_goal(goal_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Queries DB for specified Goal and returns full details as JSON data.'''

    goal = validate_and_get_by_id(Goal, goal_id)
    goal.display_full = True

    return jsonify(goal), 200
