from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify, make_response, abort
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# CREATE aka POST new task at endpoint: /tasks
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response(jsonify(dict(details="Invalid data")), 400)
    
    new_task = Task.create(request_body)
    
    db.session.add(new_task)
    db.session.commit()
    
    #COMPARE these return statement options...significance of make_response (something to do with headers but importance?)
    # return make_response(jsonify(response_body), 201)
    # return make_response(jsonify({"task": new_task.to_dict()}), 201)
    return jsonify({"task": new_task.to_dict()}), 201   

# GET ALL TASKS aka READ at endpoint /tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    #Because our Task Model is derived from db.Model we inherit some 
    #functionality such as a helper function/method called query:
    # tasks = Task.query.all()
    title_query = request.args.get("sort")

    if title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())

    elif title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return make_response(jsonify(tasks_response), 200) 

#####
# GET aka READ task at endpoint: /tasks/id 
@tasks_bp.route("/<id>", methods=["GET"])
def get_task_by_id(id):
    task = validate_task(id)

    # NOTE: Flask will automatically convert a dictionary into an HTTP response body. 
    # If we don't want to remember this exception, we can call jsonify() with the dictionary as an argument to return the result
    return jsonify({"task": task.to_dict()}), 200
    # return make_response(jsonify({"task": task.to_dict()}), 201)

# *************Could alternatively use a hash to look things up by id.  ...need to practice this later. 

@tasks_bp.route("/<id>", methods=['PUT'])
def update_task(id):
    task = validate_task(id)

    request_body = request.get_json()

    task.update(request_body)
    db.session.commit()
    return jsonify({"task": task.to_dict()}), 200
    # return make_response(jsonify({"task": f"{task_id} successfully updated"})), 200

# DELETE /tasks/id
@tasks_bp.route("<id>", methods=['DELETE'])
def delete_one_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    # return make_response(f"Task #{id} successfully deleted", 200)
    # return make_response(f"Task #{task.task_id} successfully deleted"), 200  #Do I need to jsonify this?
    # return jsonify(dict(details= f"Task {id} {task.to_dict()["title"]})), 200
    return jsonify({'details': f'Task {id} "{task.title}" successfully deleted'}), 200



#QUALITY CONTROL HELPER FUNCTION
def validate_task(id):
    try:
        id = int(id)
    except ValueError: 
        # return jsonify({}), 400     .....OR
        abort(make_response(jsonify(dict(details=f"invalid id: {id}")), 400))
        # abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(id)
    if task:
        return task

    elif not task:
        abort(make_response(jsonify(dict(message= f"task {id} not found")), 404))
        # abort(make_response({"message": f"task {id} not found"}, 404))
    
#########   
# PATCH a task at endpoint: tasks/id  #Remember PATCH is just altering one or some attributes whereas PUT replaces a record. 
@tasks_bp.route("/<id>", methods=["PATCH"])
def update_one_task(id):
    task = validate_task(id)
    request_body = request.get_json()
    task_keys = request_body.keys()

    if "title" in task_keys:
        task.title = request_body["title"]
    if "description" in task_keys:
        task.description = request_body["description"]
    if "completed_at" in task_keys:
        task.completed_at = request_body["completed_at"]

    db.session.commit()
    return make_response(f"Task# {task.task_id} successfully updated"), 200

# PATCH a task at endpoint: tasks/id/mark_complete 
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = validate_task(id)
    
    # if task.completed_at:
    task.completed_at = datetime.utcnow()

    db.session.commit()
    print(post_slack_message(task.title))


    return make_response(jsonify({"task": task.to_dict()}), 200)

# PATCH a task at endpoint: tasks/id/mark_incomplete
@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = validate_task(id)

    task.completed_at = None

    db.session.commit()
    return make_response(jsonify({"task": task.to_dict()}), 200)


def post_slack_message(text):
    slack_channel = "task-notifications"
    slack_user_name = "smiley_face"
    slack_icon_emoji = "hope-ada"

    load_dotenv()
    
    return requests.post('https://slack.com/api/chat.postMessage', 
        headers={"Authorization": os.environ.get("bearer_token")},
        json={
        'channel': slack_channel,
        'text': text,
        'icon_emoji': slack_icon_emoji,
        'username': slack_user_name
            }).json()	




    # task.completed_at = datetime.utcnow

    # if task.completed_at is None:
    #     task.completed_at = datetime.utcnow()
    # elif task.completed_at is not None:
    #     task.copleted_at = datetime.utcnow()
    



