from datetime import datetime
from xmlrpc.client import boolean
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate(input_id):
    try:
        int_id = int(input_id)
    except:
        abort(make_response({"message":f"Task {input_id} invalid"}, 400))
    task = Task.query.get(int_id)
    if not task:
        abort(make_response({"message":f"Task {int_id} not found"}, 404))
    return task

@tasks_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task(
            title=request_body["title"], 
            description=request_body["description"]
            )

        ##try these instead of using expire:
        #return make_response({
                #     "task": new_task.to_dict()
                # }, 201)
        # return {
        #         "task": new_task.to_json()
        #     }, 200

        db.session.add(new_task)
        db.session.commit()
        db.session.expire(new_task)

        return make_response(jsonify(new_task.single_dict()), 201)

    except KeyError:
        return make_response(jsonify({"details":"Invalid data"}), 400)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    # # from planets api:
    # name_query = request.args.get("name")
    # description_query = request.args.get("description")
    # order_from_sun_query = request.args.get("order_from_sun")
    # if name_query:
    #     planets = Planet.query.filter_by(name=name_query)
    # elif description_query:
    #     planets = Planet.query.filter(Planet.description.ilike("%" + description_query + "%"))
    # elif order_from_sun_query:
    #     planets = Planet.query.filter_by(order_from_sun =order_from_sun_query)
    # else:
    #     planets = Planet.query.all()
    sort_query = request.args.get("sort")

    if sort_query in ("asc","desc") :
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title).all()
        else:
            tasks = Task.query.order_by(Task.title.desc()).all()
    else: 
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return make_response(jsonify(tasks_response), 200)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate(task_id)

    return make_response(jsonify(task.single_dict()), 200)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate(task_id)
    request_body = request.get_json()
    request_body_keys = request_body.keys()

    if "title" in request_body_keys:
        task.title = request_body["title"]
    if "description" in request_body_keys:
        task.description = request_body["description"]
    if "completed_at" in request_body_keys:
        task.completed_at = request_body["completed_at"]
    elif "is_complete" in request_body_keys:
        if request_body["is_complete"] == True:
            task.completed_at = datetime.utcnow()
        elif request_body["is_complete"] == False:
            task.completed_at = None

    db.session.commit()
    db.session.expire(task)

    return make_response(jsonify(task.single_dict()), 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate(task_id)
    
    response = {"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}
# "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify(response), 200)