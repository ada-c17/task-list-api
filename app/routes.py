from app import db
from app.models.task import Task 
from flask import Blueprint, jsonify, make_response, request, abort 
from app.helper_routes import error_message


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def make_task_safely(data_dict):
    return Task.from_dict(data_dict)

	# try:
	# 	return Task.from_dict(data_dict)
	# except KeyError as err:
	# 	error_message(f"Missing key: {err}", 400)

@task_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    # name_param = request.args.get("name")
    
    # if name_param:
    #     tasks = Task.query.filter_by(name=name_param)
    # else:

    response_body = [task.to_dict() for task in tasks]
    return jsonify(response_body) 

def validate_task(id):
	try:
		id = int(id)
	except ValueError:
		error_message(f"Invalid id {id}", 400)

	task = Task.query.get(id)
		
	if task:
		return task
	error_message(f'task with id #{id} not found', 404)


@task_bp.route("", methods=["POST"])
def create_task(): 
    request_body = request.get_json()
    new_task = make_task_safely(request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict_one_task()), 201 


@task_bp.route("/<id>", methods=["GET"])
def get_task(id):
    task = validate_task(id)
    return jsonify(task.to_dict_one_task())


@task_bp.route("/<id>", methods=["DELETE"])
def delete_task(id): 
    valid_task = validate_task(id)
    task = valid_task.to_dict_one_task()
    title = task['task']['title']
    response_body = {"details": f'Task {id} "{title}" successfully deleted'}

    db.session.delete(valid_task)
    db.session.commit()
    return response_body



  




# @task_bp.route("", methods=("POST",))
# def create_task(): 
  
#     request_body = request.get_json()
#     task = make_task_safely(request_body)

# request_body = request.get_json()
# new_task = make_task_safely(request_body)

    # db.session.add(task)
    # db.session.commit()

    # return jsonify(task.to_dict()), 201 

    # return jsonify(new_task.to_dict()), 201





     

  


  



