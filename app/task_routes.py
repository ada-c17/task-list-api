from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from datetime import datetime
import requests
import os

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def send_slack_notification(task):
    slack_path = 'https://slack.com/api/chat.postMessage'
    headers = {'Authorization': f'Bearer {os.environ.get("SLACK_API_KEY")}'}
    
    query_param = {
        'channel': 'task-notifications',
        'text': f'Someone just completed {task}!'
    }

    return requests.post(slack_path, params=query_param, headers=headers)  

def validate_task(task_id):
    #this portion makes sure the input type is valid
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({'details': 'Invalid id. ID must be an integer.'}, 400))
    task = Task.query.get(task_id)

    #this portion handles whether task record exists
    if not task:
        abort(make_response({'details': 'Task id not found.'}, 404))

    return task

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    query_params = request.args
    if 'sort' in query_params:
        if request.args.get('sort') == 'desc':
            tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.order_by(Task.title)
    else:
        tasks = Task.query.all()
    
    tasks_response = [task.get_dict() for task in tasks]
    
    return jsonify(tasks_response), 200

@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json() #turns request body into python dictionary
    if 'title' not in request_body or\
        'description' not in request_body:
        return jsonify({'details': 'Invalid data'}), 400
    #creates a Task that has not been completed
    new_task = Task(title=request_body['title'], 
                    description=request_body['description'])
    #changes new_task record to include completion time if task input is already completed
    if 'completed_at' in request_body:
        new_task.completed_at=request_body['completed_at']
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task.get_dict()}), 201

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)

    return jsonify({'task': task.get_dict()})

@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    if 'title' not in request_body or\
        'description' not in request_body:
        return jsonify({'msg': f'Request must include title and description'}), 400

    task.title = request_body['title']
    task.description = request_body['description']

    if 'completed_at' in request_body:
        task.completed_at = request_body['completed_at']

    db.session.commit()
    return jsonify({'task': task.get_dict()})

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = validate_task(task_id)
    response_body = jsonify({
            'details': f'Task {task_id} "{task.title}" successfully deleted'
        }), 200
    db.session.delete(task)
    db.session.commit()
    return response_body

@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete(task_id):
    task = validate_task(task_id)
    
    task.completed_at = datetime.utcnow()

    db.session.commit()
    send_slack_notification(task.title)
    return jsonify({'task': task.get_dict()})

@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_incomplete(task_id):
    task = validate_task(task_id)
    
    task.completed_at = None

    db.session.commit()

    return jsonify({'task': task.get_dict()})
