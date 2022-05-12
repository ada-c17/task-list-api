from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from datetime import datetime
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)
client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({'details': 'Invalid data'}, 400))
    
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({'details': f'No task with id {task_id}'}, 404))

    return task


@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    new_task = Task.from_json(request_body)

    db.session.add(new_task)
    db.session.commit()

    rsp = {'task': new_task.to_json()}
    return jsonify(rsp), 201


@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    params = request.args.get('sort')
    if params == 'desc':
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif params == 'asc':
        tasks = Task.query.order_by(Task.title.asc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200


@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task = validate_task_id(task_id)
    rsp = {'task': task.to_json()}

    return jsonify(rsp), 200


@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task = validate_task_id(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'details': f'Task {task.id} \"{task.title}\" successfully deleted'}), 200


@tasks_bp.route('/<task_id>', methods=['PUT', 'PATCH'])
def update_one_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()
    task = task.from_json_to_update(request_body)

    db.session.commit()

    rsp = {'task': task.to_json()}
    return jsonify(rsp), 200


@tasks_bp.route('<task_id>/mark_complete', methods=['PATCH'])
def mark_task_complete(task_id):
    daytime_completed = datetime.now()
    task = validate_task_id(task_id)
    task.completed_at = daytime_completed

    db.session.commit()

    channel_id = 'C03EG8HQVEJ'

    try:
        result = client.chat_postMessage(
        channel=channel_id, 
        text=f'Someone just completed the task {task.title}'
    )
        logger.info(result)
    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")

    rsp = {'task': task.to_json()}
    return jsonify(rsp), 200


@tasks_bp.route('<task_id>/mark_incomplete', methods=['PATCH'])
def mark_task_incomplete(task_id):
    task = validate_task_id(task_id)
    task.completed_at = None

    db.session.commit()

    rsp = {'task': task.to_json()}
    return jsonify(rsp), 200
