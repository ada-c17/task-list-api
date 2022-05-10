from flask import Blueprint, jsonify, request, make_response, abort
from pytest import param
from app.models.task import Task
from app import db


tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

@tasks_bp.route('', methods=['POST'])
def create_a_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"])
    except:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }), 201

    
    # request_body = request.get_json()
    # new_task = Task(title, description)
    # try:
    #     new_task.title = request_body["title"]
    # except KeyError:
    #     return {"details": "Invalid data"}, 400
    # try:
    #     new_task.description = request_body["description"]
    # except KeyError:
    #         return {"details": "Invalid data"}, 400

    # db.session.commit()

    # if not new_task.completed_at:
    #     is_complete = False

    # rsp = {
    #     'id': chosen_task.title_id,
    #     'title': chosen_task.title,
    #     'description': chosen_task.description,
    #     'is_complete': is_complete
    # }
    # return jsonify(rsp), 201

@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    params = request.args
    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    tasks_response = []
    
    for task in tasks:
        tasks_response.append({
                'id': task.task_id,
                'title': task.title,
                'description': task.description,
                'is_complete': False
            })

    return jsonify(tasks_response), 200


def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify({'details': f'Invalid task id: {task_id}. Task id must be an integer'}), 400

    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        task_response = {'details': f'Could not find task id {task_id}'}
        abort(make_response(jsonify(task_response), 404))
        
    return chosen_task
    

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    return jsonify({
        "task": {
            'id': chosen_task.task_id,
            'title': chosen_task.title,
            'description': chosen_task.description,
            'is_complete': False
            }
        }), 200


@tasks_bp.route('/<task_id>', methods=['PUT'])
def put_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    
    request_body = request.get_json()
    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
        # chosen_task.completed_at = request_body["completed_at"]
    except KeyError:
        return jsonify({"details": "Request must include both title and description"}), 400
    
    db.session.commit()

    return jsonify({
        "task": {
            'id': chosen_task.task_id,
            'title': chosen_task.title,
            'description': chosen_task.description,
            'is_complete': False
            }
        }), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f"Task {chosen_task.task_id} \"{chosen_task.title}\" successfully deleted"
    }, 200

