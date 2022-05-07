from re import A
from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db
from sqlalchemy import asc, desc


task_list_bp = Blueprint("task_list", __name__, url_prefix='/tasks')

@task_list_bp.route('', methods = ['POST'])
def create_one_task():
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        rsp = {"details": "Invalid data"}
        abort(make_response(jsonify(rsp), 400))


    new_task = Task(title=request_body['title'], 
                    description=request_body['description'])
    is_complete = False
    db.session.add(new_task)
    db.session.commit()
    rsp = {
        "task":{
        "id": new_task.task_id,
        "title": new_task.title,
        "description":new_task.description,
        "is_complete": is_complete
        }
    }

    return jsonify(rsp), 201


def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg":f"Invalid id: {task_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        #rsp = {"msg": f"Could not find task with id {task_id}"}
        rsp =  {"msg": "Task not found"}
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


@task_list_bp.route('', methods = ['GET'])
def get_all_tasks():

    #params = request.args
    #if "sort" in params:
        
        #if params["sort"] == "asc":
            #p = 1
            #tasks = Task.query.order_by(asc("title"))
            #tasks = Task.query.order_by(Task.title.asc())
            #tasks = Task.query.order_by("Task.title asc")
        #elif params["sort"] is "desc":
    #else:
        #p = 2

    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        if task.completed_at is None:
            is_complete = False
        else:
            is_complete = True

        tasks_response.append({
            'id': task.task_id,
            'title': task.title,
            'description': task.description,
            'is_complete': is_complete
        })

    #check params for sorting
    params = request.args
    sort_type = None
    if "sort" in params:
        if params["sort"] == "asc":
            #ascending
            sort_type = "A"
        else:
            #descending
            sort_type = "D"

    if sort_type == "A":
        tasks_response = (sorted(tasks_response, key=lambda i: i['title']))

    elif sort_type == "D":
        tasks_response = (sorted(tasks_response, key=lambda i: i['title'], reverse = True))
    
    return jsonify(tasks_response)




@task_list_bp.route('/<task_id>', methods = ['PUT'])
def update_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    request_body = request.get_json()
    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
        #completed_at
    except KeyError:
        return{
            "msg": "title and description are required"
        }, 400
    db.session.commit()

    if chosen_task.completed_at is None:
        is_complete = False
    else:
        is_complete = True

    rsp = {
        "task": {
        'id': chosen_task.task_id,
        'title': chosen_task.title,
        'description': chosen_task.description,
        'is_complete': is_complete
        }
        #"msg": f"task #{chosen_task.id} successfully replaced"
    }
    return jsonify(rsp), 200

@task_list_bp.route('/<task_id>', methods = ['DELETE'])
def delete_task(task_id):

    chosen_task = get_task_or_abort(task_id)

    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f"Task {chosen_task.task_id} \"{chosen_task.title}\" successfully deleted"
    }, 200



