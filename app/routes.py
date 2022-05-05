from flask import Blueprint, jsonify, abort, make_response
from app.models.task import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def validate_task(task_id):
    #this portion makes sure the input type is valid
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({'message': f'Invalid id: "{task_id}". ID must be an integer.'}, 400))
    task = Task.query.get(task_id)

    #this portion handles whether task record exists
    if not task:
        abort(make_response({'message': f'Task id: "{task_id}" not found.'}, 400))

    return task    

@tasks_bp.route('', methods=['GET'])
def handle_tasks():
    tasks = Task.query.all()
    tasks_response = []

    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
    return jsonify(tasks_response)

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)

    return jsonify({'task':
        {'id': task.task_id,
        'title': task.title,
        'description': task.description,
        'is_complete': False}
    })
