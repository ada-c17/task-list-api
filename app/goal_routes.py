from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app.task_routes import validate_task
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

@goals_bp.route('', methods=['GET'])
def get_goals():
    goals = Goal.query.all()
    goals_response = [goal.get_dict() for goal in goals]
    
    return jsonify(goals_response), 200

@goals_bp.route('', methods=['POST'])
def create_goal():
    request_body = request.get_json()

    if 'title' not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal(title=request_body['title'])

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({'goal': new_goal.get_dict()}), 201

@goals_bp.route('/<goal_id>', methods=['PUT'])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    if request.method == 'PUT':
        request_body = request.get_json()
        goal.title = request_body['title']
        
    db.session.commit()
    return jsonify({'goal': goal.get_dict()}), 200

@goals_bp.route('<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return jsonify({'goal':goal.get_dict()}), 200

@goals_bp.route('<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    response_body = jsonify({
        'details': f'Goal {goal_id} "{goal.title}" successfully deleted'
        })
    db.session.delete(goal)
    db.session.commit()
    return response_body

@goals_bp.route('/<goal_id>/tasks', methods=['POST'])
def create_task_for_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    
    #check that the request body includes key-value pair where value is a list
    try:
        task_ids = request_body['task_ids']
    except KeyError:
        abort(make_response({'details': 'Request body must include a list of task ids'}, 400))
    
    for task_id in task_ids:   
        #check that each task_id is valid and task exists in database
        task = validate_task(task_id)
        task.goal_id = goal.goal_id
        
    db.session.commit()

    return jsonify({
        'id': goal.goal_id,
        'task_ids': request_body['task_ids']
        }), 200

@goals_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_tasks_for_goal(goal_id):
    goal = validate_goal(goal_id)
    tasks_response = [task.get_dict() for task in goal.tasks]
    
    response_body = goal.get_dict()
    response_body['tasks'] = tasks_response
    return jsonify(response_body), 200