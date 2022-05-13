from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app import db
from app.models.task import Task, validate_task
from datetime import datetime
import os 


tasks_bp = Blueprint ('tasks_bp', __name__, url_prefix = '/tasks')

def is_completed(completed_at):
    if completed_at is None:
        return False
    else: 
        return True



@tasks_bp.route('', methods=['POST'])
def create_a_task():
    request_body = request.get_json()
    if not 'description' in request_body:
        return ({'details': 'Invalid description'}, 400)
    elif not 'title' in request_body:
        return ({'details': 'Description does not exist'}, 404)

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

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
            'id' :task.task_id,
            'title': task.title,
            'description': task.description,
            'is_complete': is_completed(task.completed_at)
            }) , 200
            
    return jsonify(tasks_response)



@tasks_bp.route('/<task_id>',methods = ['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)
    if task.goal_id:
        response_body = {"task":{
            'id' :task.task_id,
            'title': task.title,
            'goal_id':task.goal_id,
            'description': task.description,
            'is_complete': is_completed(task.completed_at)
        }}
    else:
        response_body = {
            'id' :task.task_id,
            'title': task.title,
            'description': task.description,
            'is_complete': is_completed(task.completed_at)
        }

    return jsonify(response_body), 200



@tasks_bp.route('/<task_id>', methods = ['PUT'])
def update_one_task(task_id):
    validate_task(task_id)
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
    validate_task(task_id)
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
    validate_task(task_id)
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
    validate_task(task_id)
    chosen_task = Task.query.get(task_id)
    if chosen_task is None:
        response_body = {"msg": f"{task_id} is an invalid id"}
        return jsonify(response_body), 404
    
    db.session.delete(chosen_task)
    db.session.commit()

    response_body = {'details':f'Task {chosen_task.task_id} "{chosen_task.title}" successfully deleted'}

    return jsonify(response_body), 200

