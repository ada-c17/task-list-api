from flask import Blueprint,jsonify, request, make_response, abort
from app.models.task import Task
from app import db

tasks_bp = Blueprint("task", __name__,url_prefix="/tasks")

@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400
    new_task = Task(title=request_body["title"],
                  description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    response = {
        "task":{
        "id":new_task.task_id,
        "title":new_task.title,
        "description": new_task.description,
        "is_complete": bool(new_task.completed_at) }
    }
    return jsonify(response), 201

@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    params = request.args
    if "title" in params and "description" in params:
        title_exp = params["title"]
        description_exp=params["age"]
        tasks = Task.query.filter_by(title = title_exp, description = description_exp)
    elif "title" in params:
        title_exp = params["title"]
        tasks = Task.query.filter_by(title = title_exp)
    elif "description" in params:
        description_exp=params["age"]
        tasks = Task.query.filter_by(description = description_exp)
    else:
        tasks= Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append({
            'id':task.task_id,
            'title':task.title,
            'description':task.description,
            'is_complete': bool(task.completed_at)
        })
    return jsonify(task_response)


def get_task_or_abort(task_id):
    try:
        task_id = int (task_id)
    except ValueError:
        rsp =  {"msg": f"Invalid id:{task_id}"}
        abort( make_response (jsonify(rsp), 400))
        
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        abort( make_response({"massage": f" task {task_id} not found"}, 404))
    
    return chosen_task

# get one task
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    request_body = request.get_json()
    rsp = {
        "task":{
        'id':chosen_task.task_id,
        'title':chosen_task.title,
        'description':chosen_task.description,
        'is_complete':bool(chosen_task.completed_at)}
    }

    return jsonify(rsp), 200

# update chosen task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    request_body = request.get_json()

    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]

    except KeyError:
        return {
            "msg": "title, and description are required"
        },404

    db.session.commit()

    rsp = {
        "task":{
        'id':chosen_task.task_id,
        'title':chosen_task.title,
        'description':chosen_task.description,
        'is_complete':bool(chosen_task.completed_at)}
    }

    return jsonify(rsp), 200

    # return make_response(f"Task #{chosen_task.task_id} successfully updated"), 200


# delete chosen task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    db.session.delete(chosen_task)
    db.session.commit()

    response_body = { 
        "details":f'Task {chosen_task.task_id} "{chosen_task.title}" successfully deleted'
    }

    return jsonify(response_body), 200
