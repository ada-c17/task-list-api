
from wsgiref.util import request_uri
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import asc
from datetime import datetime




tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        return abort(make_response({"details": "Invalid data"}, 400))
    task = Task.query.get(task_id)

    if not task:
        return abort(make_response({"message" : f"task given is invalid"}, 404))
    return task

@tasks_bp.route("", methods=["GET"])
def get_all_task():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    
    return make_response(jsonify(tasks_response), 200)
@tasks_bp.route("<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)
    return jsonify({"task": task.to_json()}), 200
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.create_task(request_body)
    
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task": new_task.to_json()}), 201
@tasks_bp.route("<task_id>", methods=['PUT'])
def update_one_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body['title']
    task.description = request_body['description']
    db.session.commit()
    
    return make_response(jsonify({"task" : task.to_json()}), 200)

@tasks_bp.route('<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": 'Task 1 Go on my daily walk successfully deleted'} ), 200)
    

@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_task_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.now()
    db.session.commit()

    return make_response(jsonify({"task" : task.to_json()}))

@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_task_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    return make_response(jsonify({"task" : task.to_json()})) 






# def error_message(message, status_code):
#     abort(make_response({"message":message}, status_code))


# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort (make_response(f"Task {task_id} invalid", 400))

#     task = Task.query.get(task_id)
#     if not task:
#         abort (make_response({"message" : f"Task given is invalid"}, 404))

#     return task

# def validate_request(request):
#     request_body = request.get_json()
#     try:
#         request_body["title"]
#         request_body["description"]
#     except KeyError:
#         abort (make_response({"details" : f"Invalid data"}, 404))  
#     return request_body      
# # VALIDATE ID
# def validate_id(task_id):
#     try:
#         task_id = int(task_id)
#     except ValueError:
#         abort(make_response(jsonify(f"Task {task_id} is invalid"), 400))
#     task = Task.query.get(task_id)
#     if not task:
#         abort(make_response(jsonify(f"Task {task_id} not found"), 404))
#     return task


# #POST

# @tasks_bp.route("", methods=["POST"])
# def create_new_task():
#     request_body = request.get_json()
#     request_body = validate_request(request)
#     new_task = Task(
#         title=request_body["title"],
#         description= request_body["description"],
#         completed_at= request_body["completed_at"] if "completed_at" in request_body else None
#     )        
    
#     # if :
#     #         completion_time = request_body["completed_at"]
#     #         new_task = Task(
#     #             title=request_body["title"],
#     #             description=request_body["description"],
#     #             completed_at = completion_time
#     #         )
#     # except KeyError:
#     #         new_task = Task(
#     #             title=request_body["title"],
#     #             description=request_body["description"]
#     #         )
#     db.session.add(new_task)
#     db.session.commit()

#     return make_response(jsonify({"message" : f"Task was successfully created"}, 201))

# #GET

# @tasks_bp.route("", methods=("GET",))
# def read_all_books():
#     #get query from url
#     title_param = request.args.get("title")
#     description_param = request.args.get("description")
#     is_complete_param =request.args.get("is_complete")
#     sort_param = request.args.get("sort")

#     #Initialize
#     tasks = Task.query

#     #search
#     if title_param:
#         tasks = tasks.filter_by(name=title_param)
#         tasks = tasks.filter_by(title=title_param)
#     if description_param:
#         tasks = tasks.filter_by(description=description_param)
#     if is_complete_param:
#         tasks = tasks.filter_by(color=is_complete_param)
#     if sort_param == "asc":
#         tasks = tasks.order_by(Task.title.asc())
#     elif sort_param == "desc":
#         tasks = tasks.order_by(Task.title.desc())
#     # execute the search and return all records that meet the criterium
#     tasks = tasks.all()
#     tasks_response = []
#     for task in tasks:
#         tasks_response.append(task.to_dict())
#     return jsonify(tasks_response)


# @tasks_bp.route("/<task_id>", methods=["GET"])
# def index_single_task(task_id):
#     task = validate_task(task_id)
#     return  make_response(jsonify({"task": task.to_dict()}), 200)


# @tasks_bp.route("/<task_id>", methods=["GET"])
# def read_one_task(task_id):
#     task = validate_task(task_id)
#     return task.to_dict()

# #PUT

# @tasks_bp.route("/<task_id>", methods=["PUT"])
# def update_task(task_id):
#     task = validate_task(task_id)
#     request_body = request.get_json()
#     task.title = request_body["title"]
#     task.description = request_body["description"]
#     task.completed_at = request_body["completed_at"]
#     db.session.commit()
#     return make_response(jsonify(f"Task #{task.id} successfully updated"))

# #DELETE
# @tasks_bp.route("/<task_id>", methods=["DELETE"])
# def delete_task(task_id):
#     task = validate_task(task_id)

#     db.session.delete(task)
#     db.session.commit()
#     return make_response(jsonify(f"Task #{task.id} successfully deleted"))    
#     # {'completed_at': None, 'description': 'Notice something new every day', 'is_complete': False, 'task_id': 1, 'title': 'Go on my daily walk #x1F3DE'} !=
#     # {'id': 1, 'title': 'Go on my daily walk #x1F3DE', 'description': 'Notice something new every day', 'is_complete': False}


# # MARK COMPLETE
# @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_complete(task_id):
#     task = validate_id(task_id)
#     task.completed_at = date.today()
#     db.session.commit()
#     return make_response({"task": task.to_dict()})

# # MARK INCOMPLETE
# @tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(task_id):
#     task = validate_id(task_id)
#     task.completed_at = None
#     db.session.commit()
#     return make_response({"task": task.to_dict()}) 
# #PATCH



# # def index_all_tasks():
# #     tasks = Task.query.all()
# #     result_list = [task.to_dict() for task in tasks]

# #     return make_response(jsonify(result_list), 200)
