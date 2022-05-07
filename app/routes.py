from urllib import response
from xmlrpc.client import DateTime
from sqlalchemy import null, true
import datetime
from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify, make_response, abort


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        return abort(make_response(jsonify(f"Task {task_id} is invalid"), 400))

    task = Task.query.get(task_id)

    if not task:
        return abort(make_response(jsonify(f"Task {task_id} does not exist"), 404))
    return task

# @tasks_bp.route("", method=["POST"])
# def create_task():
#     request_body = request.get_json()
#     new_task = Task.create(request_body)

#     db.session.add(new_task)
#     db.session.commit()

#     return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)


# def completed_check(task_id):
#     # task = validate_task(task_id)
#     if task_id.completed_at == None:
#         return False
#     return True
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    # new_task = Task(title=request_body["title"],
    #                 description=request_body["description"])

    # new_task = Task.create(request_body)
    # if task.completed_at != None:
    #     task.completed_at = None
    # if task.completed_at == None:
    #     task.completed_at = datetime.datetime.now()
    # valid completed at == True
    # if Task

    try:
        new_task = Task.create(request_body)
        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]
        db.session.add(new_task)
        db.session.commit()

    except KeyError:
        return abort(make_response(jsonify({"details": "Invalid data"}), 400))

    return make_response(jsonify(new_task.to_json()), 201)


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    # newlist = sorted(list_to_be_sorted, key=lambda d: d['name'])
    # sort = sorted(Task.query.all(), key=lambda d: d["title"])
    # User.query.order_by(User.username).all()
    asc_query = request.args.get("sort")
    if asc_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif asc_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    # tasks_response = [task.to_json() for task in tasks]
    tasks_response = []

    for task in tasks:
        complete = None
        if task.completed_at == None:
            complete = False
        else:
            complete = True
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": complete
        })
        # if task.completed_at == None:
        #     tasks_response[0]["is_complete"] = False
        # else:
        #     tasks_response[0]["is_complete"] = True
    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = validate_task(task_id)
    return make_response(jsonify(task.to_json()), 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    # try:
    #     Task.update(request_body)
    task.title = request_body["title"]
    task.description = request_body["description"]
    # # new_update = Task.update(request_body)
    db.session.commit()
    # except KeyError:
    #     return abort(make_response(jsonify("Missing information")), 400)

    return make_response(jsonify(task.to_json()), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200)

    # "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    # try:
    #     Task.update(request_body)
    #     db.session.commit()
    # except KeyError:
    #     return abort(make_response(jsonify("Missing information")), 400)

    # return new_update.to_json(), 200
    return {
        "task": new_update.to_json()
    }, 200

# for patch,  i am only trying to patch the "completed_at" portion
# 1.) change the content inside completed_at
# 2.) once its changed it is no longer false
# 3.) convert it again into boolean


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_update(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    if task.completed_at == None:
        task.completed_at = datetime.datetime.now()

    db.session.commit()
    # except KeyError:
    #     return abort(make_response(jsonify("Missing information")), 400)
    return make_response(jsonify(task.to_json()), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_update(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    if task.completed_at != None:
        task.completed_at = None

    db.session.commit()
    # except KeyError:
    #     return abort(make_response(jsonify("Missing information")), 400)
    return make_response(jsonify(task.to_json()), 200)
# /tasks/1/mark_incomplete


"""
    @books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(f"Book #{book.id} successfully updated")"""

# @books_bp.route("", methods=["GET"])
# def handle_books():
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })
#     return jsonify(books_response)
