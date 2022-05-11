from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({'details': 'Invalid id. ID must be an integer.'}, 400))
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({'details': 'goal id not found.'}, 404))

    return goal

def goal_response(goal):
    return {
        'id': goal.goal_id,
        'title': goal.title
    }

@goals_bp.route('', methods=['GET'])
def get_goals():
    goals = Goal.query.all()
    goals_response = []

    for goal in goals:
        goals_response.append(goal_response(goal))
    
    return jsonify(goals_response)

@goals_bp.route('', methods=['POST'])
def create_goal():
    request_body = request.get_json()

    if 'title' not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal(title=request_body['title'])

    db.session.add(new_goal)
    db.session.commit()

    return {'goal': goal_response(new_goal)}, 201

@goals_bp.route('/<goal_id>', methods=['DELETE', 'PUT', 'GET'])
def handle_one_goal(goal_id):
    goal = validate_goal(goal_id)
    response_body = {'goal': goal_response(goal)}

    if request.method == 'DELETE':
        response_body = jsonify({
        'details': f'Goal {goal_id} "{goal.title}" successfully deleted'
        })
        db.session.delete(goal)
        
    elif request.method == 'PUT':
        request_body = request.get_json()
        goal.title = request_body['title']
        response_body = {'goal': goal_response(goal)}
    
    elif request.method == 'GET':
        return response_body
        
    db.session.commit()
    return response_body

@goals_bp.route('/<goal_id>/tasks', methods=['POST'])
def create_task_for_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    task_ids = request_body['task_ids']
    
    for task_id in task_ids:   
        task = Task.query.get(task_id)
        task.goal_id = goal.goal_id
        
    db.session.commit()

    return {
        'id': goal.goal_id,
        'task_ids': request_body['task_ids']
        }

@goals_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_tasks_for_goal(goal_id):
    goal = validate_goal(goal_id)
    tasks_response = []
    for task in goal.tasks:
        is_complete = False
        if task.completed_at:
            is_complete = True
        tasks_response.append({
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete
        })
    
    return {
        'id': goal.goal_id,
        'title': goal.title,
        'tasks': tasks_response
        }