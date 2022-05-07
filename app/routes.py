from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint ('tasks_bp', __name__, url_prefix = '/tasks')

def validate_input(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({'details': 'Invalid id data'}, 400))
    tasks = Task.query.all()
    for task in tasks:
        if task_id == task.id:
            return task
        abort(make_response ({'details': f'This {task_id} does not exist'}, 404))

def validate_if_completed(completed_at):
    if completed_at is None:
        return False
    else: 
        return True

@tasks_bp.route('', methods=['POST'])
def create_a_task():
    print ("entro")
    request_body = request.get_json()
    if not 'description' in request_body:
        return ({'details': 'Invalid data'}, 400)
    elif not 'title' in request_body:
        return ({'details': 'Invalid data'}, 400)
    new_task = Task(title=request_body['title'],
                    description=request_body['description'])
    
    db.session.add(new_task)
    db.session.commit()

    return {'task': {  
            "id" :new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": validate_if_completed(new_task.completed_at)}} , 201