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

    if not Task:
        return abort(make_response(jsonify(f"Planet {task_id} does not exist"), 404))
    return task

# @tasks_bp.route("", method=["POST"])
# def create_task():
#     request_body = request.get_json()
#     new_task = Task.create(request_body)

#     db.session.add(new_task)
#     db.session.commit()

#     return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)


# class Task:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description


# tasks = [
#     Task(1, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Task(2, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Task(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ]


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
        })
        if task.completed_at == None:
            tasks_response[0]["is_complete"] = False
        else:
            tasks_response[0]["is_complete"] = True
    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    db.session.add(new_task)
    db.session.commit()
    return make_response(f"Task {new_task.title} successfully created", 201)

    # planet_query = request.args.get("name")
    # color_query = request.args.get("color")
    # if planet_query:
    #     planets = Planet.query.filter_by(name=planet_query)
    # elif color_query:
    #     planets = Planet.query.filter_by(color=color_query)
    # else:
    tasks = Task.query.all()

    planets_response = [task.to_json() for task in tasks]
# def get_all_tasks():
#     tasks_response = []
#     for task in tasks:
#         tasks_response.append({
#             "id": task.id,
#             "title": task.title,
#             "description": task.description
#         })
#     return jsonify(tasks_response)


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
