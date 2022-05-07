from sqlalchemy import null
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


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []
    asc_query = request.args.get("title")
    if asc_query:
        tasks = Task.query.filter_by()
    tasks = Task.query.all()

    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description
        })
        if task.completed_at == None:
            tasks_response[0]["is_complete"] = False
        else:
            tasks_response[0]["is_complete"] = True
    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = validate_task(task_id)
    return make_response(jsonify(task.to_json()), 200)


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    # new_task = Task(title=request_body["title"],
    #                 description=request_body["description"])

    # new_task = Task.create(request_body)
    try:
        new_task = Task.create(request_body)
        db.session.add(new_task)

        db.session.commit()
    except KeyError:
        return make_response(jsonify({"details": "Invalid data"})), 400

    # is_complete=request_body["is_complete"])
    # db.session.add(new_task)
    # db.session.commit()
    return new_task.to_json(), 201


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
