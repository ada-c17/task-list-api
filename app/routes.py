from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify, make_response, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# CREATE aka POST new task at endpoint: /tasks
@tasks_bp.route("", methods=["POST"])
def create_task():
    #This will take the contents of the request body and turn it 
    # into lists and dictionaries and give you the return value.
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response(jsonify(dict(details="Invalid data")), 400)

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"])

    db.session.add(new_task)
    db.session.commit()

# How can I avoid repeating this response body over and over? 
# Use a method to turn the response into a dictionary then jsonify. 
# SEE to_dict() method in task.py ...confused about to_json()...same thing?
    response_body = {
        "task":
            {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False if new_task.completed_at == None else True  ##Confused about what this should be...False?? It is optional
            }
        }
    
    #COMPARE these return statement options...significance of make_response (something to do with headers but importance?)
    # return make_response(jsonify(response_body), 201)
    # return make_response(jsonify({"task": new_task.to_dict()}), 201)
    return jsonify({"task": new_task.to_dict()}), 201   #Although you need to include "task" in the respond per the tests. 

# GET ALL TASKS aka READ at endpoint /tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_list = []
    #Because our Task Model is derived from db.Model we inherit some 
    #functionality such as a helper function/method called query:
    tasks = Task.query.all()

#ALTERNATIVE APPROACH TO LIST COMPREHENSION ACTUALLY USED FURTHER BELOW. 
    for task in tasks:  # We iterate over all tasks in tasks so we can collect their data and format it into a response
        # tasks_list.append(
        #     {
        #         "id": task.task_id, 
        #         "title": task.title,
        #         "description": task.description,x
        #         "is_complete": False if task.completed_at == None else True  ##Confused about what this should be...False?? It is optional
        # }
        # )
    # A more streamlined approach is to use class method to_dict() from task.py:
        tasks_list.append(task.to_dict())

    return jsonify(tasks_list) # By default, a response with no specified status code returns 200 OK

    #tasks_list contains a list of task dictionaries. 
    # To turn it into a Response object, we pass it into jsonify(). 
    # This will be our common practice when returning a list of something. 
    # When we are returning strings or dictionaries, we can use make_response, which we'll learn about later.

#####
# GET aka READ task at endpoint: /tasks/id 
@tasks_bp.route("/<id>", methods=["GET"])
def get_task_by_id(id):
    task = validate_task(id)

    # Initial approach:
    # return {"task":{
    #         "id": task.task_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": False if task.completed_at == None else True  ##Confused about what this should be...False?? It is optional
    #     }}
    # NOTE: Flask will automatically convert a dictionary into an HTTP response body. 
    # If we don't want to remember this exception, we can call jsonify() with the dictionary as an argument to return the result
    #So alternatively:
    # return jsonify(task.to_dict())
    return jsonify({"task": task.to_dict()}), 201
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
#####


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

    if "name" in task_keys:
        task.name = request_body["name"]
    if "color" in   task_keys:
        task.color = request_body["color"]
    if "personality" in task_keys:
        task.personality = request_body["personality"]

    db.session.commit()
    return make_response(f"Task# {task.task_id} successfully updated"), 200








