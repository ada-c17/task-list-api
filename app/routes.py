from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db


task_list_bp = Blueprint("task_list", __name__, url_prefix='/tasks')

@task_list_bp.route('', methods = ['POST'])
def create_one_task():
    request_body = request.get_json()
    new_task = Task(title=request_body['title'], 
                    description=request_body['description'])
    is_complete = False
    db.session.add(new_task)
    db.session.commit()
    return{
        "task":{
        "id": new_task.task_id,
        "title": new_task.title,
        "description":new_task.description,
        "is_complete": is_complete
        #,
       # "msg": f"Successfully created task with id {new_task.task_id}"
    }}, 201


def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg":f"Invalid id: {task_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        rsp = {"msg": f"Could not find task with id {task_id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_task

@task_list_bp.route('/<task_id>', methods = ['GET'])
def get_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    if chosen_task.completed_at is None:
        is_complete = False
    else:
        is_complete = True

    rsp = {'task':{
        'id': chosen_task.task_id,
        'title': chosen_task.title,
        'description': chosen_task.description,
        'is_complete': is_complete
    }}
    return jsonify(rsp), 200

@task_list_bp.route('/<task_id>', methods = ['DELETE'])
def delete_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {task_id}"}
        return jsonify(rsp), 400

    chosen_task = Task.query.get(task_id)
    if chosen_task is None:
        rsp = {"msg": f"Could not find task with id: {task_id}"}
        return jsonify(rsp), 404

    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f"Task {chosen_task.task_id} \"{chosen_task.title}\" successfully deleted"
    }, 200



