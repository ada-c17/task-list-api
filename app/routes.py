from email.policy import default
from turtle import title
from flask import Blueprint, make_response,request,jsonify,abort
from sqlalchemy import asc, false, null, true
from app import db
from app.models.task import Task
from sqlalchemy import func
from datetime import datetime

# registering my blueprint
tasks_bp=Blueprint("tasks",__name__,url_prefix="/tasks", )

# helper function to check if id is correct
def validate_task(task_id):
    # handling invalid planet_id input
    try:
        task_id=int(task_id)
    except:
        abort(make_response({"msg":f"Task # {task_id} is invalid id "},400)) 
    
    #read task id 
    task=Task.query.get(task_id)
    if task is None:
        abort(make_response({"msg":f"Task # {task_id} not found "},404)) 
    
    return task


# helper function to check request body
def check_request_body():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details":f"Invalid data"}, 400))
    return request_body

# create new task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = check_request_body()
    
    new_task=Task(
        title=request_body["title"],
        description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    rsp={
        "task": {
            "id": new_task.task_id,
             "title": new_task.title,
             "description": new_task.description,
             "is_complete": False
             }
             }
    return jsonify(rsp),201         
   
@tasks_bp.route("", methods=["GET"])
def get_tasks():  

    tasks = Task.query.all()
    
    # building planet response
    tasks_response = [] 
    
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete":False
        })

    # query parameters
    params=request.args #this returns the value of the query param if it was set, or None if the query param is not found.

    if "sort" in params and params["sort"]=="asc":
        tasks_response.sort(key=lambda x:x["title"])
    elif "sort" in params and params["sort"]=="desc":
        tasks_response.sort(key=lambda x:x["title"], reverse=True)  

    return jsonify(tasks_response)   


# get one task
@tasks_bp.route("/<task_id>", methods=["GET"]) 
def get_one_task(task_id):
    task=validate_task(task_id)
    return {
        "task": {
        "id" : task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete":False}
        }, 200  

#update a task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task=validate_task(task_id)
    request_body=check_request_body()

    task.title=request_body["title"]
    task.description=request_body["description"]
    task.completed_at=request_body.get("completed_at", None)

    db.session.commit()

    rsp={
        "task": {
            "id": task.task_id,
             "title": task.title,
             "description": task.description,
             "is_complete": task.completed_at !=None
             }
             }
    return jsonify(rsp),200


# delete a task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task=validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return (make_response({"details":f"Task {task_id} \"Go on my daily walk 🏞\" successfully deleted"}), 200)    


# Creating Custom Endpoints   
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_complete_task(task_id):
    task=validate_task(task_id)
    task.completed_at= datetime.utcnow()

    db.session.commit()

    rsp={
        "task": {
            "id": task.task_id,
             "title": task.title,
             "description": task.description,
             "is_complete": task.completed_at != None
             }
        }

    return (rsp),200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_incomplete_task(task_id):
    task=validate_task(task_id)
    task.completed_at= None

    db.session.commit()
    rsp={
        "task": {
            "id": task.task_id,
             "title": task.title,
             "description": task.description,
             "is_complete": task.completed_at != None
             }
             }
    return ((rsp),200)    