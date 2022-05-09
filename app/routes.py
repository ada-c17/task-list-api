from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app import db
from app.models.task import Task
from datetime import datetime
import os 


tasks_bp = Blueprint ('tasks_bp', __name__, url_prefix = '/tasks')

def validate_input(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({'details': 'Invalid id data'}, 400))
    tasks = Task.query.all()
    for task in tasks:
        if task_id == task.task_id:
            return task
    abort(make_response ({'details': 'This task id does not exist'}, 404))

def is_completed(completed_at):
    if completed_at is None:
        return False
    else: 
        return True

@tasks_bp.route('', methods=['POST'])
def create_a_task():
    request_body = request.get_json()
    if not 'description' in request_body:
        return ({'details': 'Invalid data'}, 400)
    elif not 'title' in request_body:
        return ({'details': 'Invalid data'}, 400)

    if not "completed_at" in request_body:
        new_task = Task(title=request_body['title'],
                    description=request_body['description'])
    else: 
        new_task = Task(title=request_body['title'],
                    description=request_body['description'],
                    completed_at = request_body['completed_at'])
    
    db.session.add(new_task)
    db.session.commit()

    return {'task': {  
            'id' :new_task.task_id,
            'title': new_task.title,
            'description': new_task.description,
            'is_complete': is_completed(new_task.completed_at)}} , 201

@tasks_bp.route("", methods=['GET'])
def get_all_tasks():
    sort_query = request.args.get('sort')
    if sort_query == 'desc':
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.order_by(Task.title)

    # title_query = request.args.get('title')
    # if title_query:
    #     tasks = Task.query.filter_by(title=title_query)
    # else:
    #     tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
            'id' :task.task_id,
            'title': task.title,
            'description': task.description,
            'is_complete': is_completed(task.completed_at)
            }) , 201
            
    return jsonify(tasks_response)

@tasks_bp.route('/<task_id>',methods = ['GET'])
def get_one_task(task_id):
    task = validate_input(task_id)
    response_body = {
        'id' :task.task_id,
        'title': task.title,
        'description': task.description,
        'is_complete': is_completed(task.completed_at)
    }
    return jsonify(response_body), 200

@tasks_bp.route('/<task_id>', methods = ['PUT'])
def update_one_task(task_id):
    validate_input(task_id)
    chosen_task = Task.query.get(task_id)
    request_body = request.get_json()
    try:
        chosen_task.title = request_body['title']
        chosen_task.description = request_body['description']
    except KeyError:
        return {'msg':'title and description are required'} ,404

    if 'completed_at' in request_body:
        chosen_task.completed_at = request_body['completed_at']

    db.session.commit()
    
    return {'task': {  
            'id' :chosen_task.task_id,
            'title': chosen_task.title,
            'description': chosen_task.description,
            'is_complete': is_completed(chosen_task.completed_at)}} , 200


@tasks_bp.route('/<task_id>/mark_complete', methods = ['PATCH'])
def complete_one_task(task_id):
    validate_input(task_id)
    chosen_task = Task.query.get(task_id)
    chosen_task.completed_at= datetime.utcnow()
    db.session.commit()
    slack_message = f'Someone just completed the task {chosen_task.title}'
    requests.post(f'https://slack.com/api/chat.postMessage?channel=task-list&text={slack_message}',
            headers = {'Authorization': f'Bearer {os.environ.get("SLACK_BOT_TOKEN")}'})

    return {'task': {  
            'id' :chosen_task.task_id,
            'title': chosen_task.title,
            'description': chosen_task.description,
            'is_complete': is_completed(chosen_task.completed_at)}} , 200

@tasks_bp.route('/<task_id>/mark_incomplete', methods = ['PATCH'])
def incomplete_one_task(task_id):
    validate_input(task_id)
    chosen_task = Task.query.get(task_id)
    chosen_task.completed_at= None
    db.session.commit()
    
    return {'task': {  
            'id' :chosen_task.task_id,
            'title': chosen_task.title,
            'description': chosen_task.description,
            'is_complete': is_completed(chosen_task.completed_at)}} , 200



@tasks_bp.route('/<task_id>',methods = ['DELETE'])
def delete_task(task_id):
    validate_input(task_id)
    chosen_task = Task.query.get(task_id)
    if chosen_task is None:
        response = {"msg": f" This is an invalid id -{task_id}-"}
        return jsonify(response), 404
    
    db.session.delete(chosen_task)
    db.session.commit()

    return{'details':f'Task {chosen_task.task_id} "{chosen_task.title}" successfully deleted'}, 200

