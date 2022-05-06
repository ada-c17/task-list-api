from os import abort

from sqlalchemy import true
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request


# ---- CREATING BLUEPRINT INSTANCE---- # 
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


# ---- HELPER FUNCTIONS ---- #

def validate_task(task_id):
    # Check if task_id is a valid integer
    try:
        task_id = int(task_id)
    except:
        # If it's not, 400 response code
        abort(make_response({"message" : f"Task {task_id} is invalid."}, 400))

    # Search for this task_id in the Task Blueprint
    task = Task.query.get(task_id)

    # If this specific task isn't found, 404 response code
    if not task:
        abort(make_response({"message" : f"This task is not found."}, 404))
    # If task found, return it 
    return task


# def format_response_body():
    
#     task_instance = Task

#     if task_instance.completed_at:
#         completed_task = True
#     else:
#         completed_task = False
    
#     task_response_body = {
#         "id": task_instance.task_id,
#         "title": task_instance.title,
#         "description": task_instance.description,
#         "is_complete": completed_task
#     }

#     return task_response_body



# ---- ROUTE FUNCTIONS ---- #

# class Task(db.Model):
#     task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String)
#     description = db.Column(db.String)
#     completed_at = db.Column(db.DateTime, nullable=True)




# ---- CREATE A TASK ---- #
@tasks_bp.route("", methods=["POST"])
def create_task():

    request_body = request.get_json()

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])


    # Returned response body should be a dictionary of dictionaries
    # {
    #     "task": {
    #         "id": 1,
    #         "title": "A Brand New Task",
    #         "description": "Test Description",
    #         "is_complete": false
    #     }
    # }


    # response_body = jsonify({ "task" :
    #     {
    #         "id" : new_task.task_id,
    #         "title" : new_task.title,
    #         "description" : new_task.description,
    #         "is_complete" : False
    #     }
        
    # })

    db.session.add(new_task)
    db.session.commit()

    # NEED TO FIX THIS RESPONSE
    # return make_response({response_body}, 201)
    response_body = new_task.format_response_body()

    # return response_body
    return jsonify({"task": response_body})


# # ---- GET ALL TASKS ---- #
# @tasks_bp.route("", methods=["GET"])
# def get_all_tasks():
    
#     response_body = []

#     tasks = Task.query.all()

    # for task in tasks:
    #     if task.completed_at == None:
    #         response_body.append(
    #             {
    #                 "id" : task.task_id,
    #                 "title" : task.title,
    #                 "description" : task.description,
    #                 "is_complete" : False
    #             }
    #         )
    #     else:
    #         response_body.append(
    #             {
    #                 "id" : task.task_id,
    #                 "title" : task.title,
    #                 "description" : task.description,
    #                 "is_complete" : True
    #             }
    #         )


    # Returned response body should be a list of dictionaries:
    # [
    #     {
    #         "id": 1,
    #         "title": "Example Task Title 1",
    #         "description": "Example Task Description 1",
    #         "is_complete": false
    #     },
    #     {
    #         "id": 2,
    #         "title": "Example Task Title 2",
    #         "description": "Example Task Description 2",
    #         "is_complete": false
    #     }
    # ]



    # return make_response({"task": response_body}, 201)
    # return {"tasks": response_body}, 201
    # return jsonify(response_body)




# ---- GET ONE TASK ---- #
# @tasks_bp.route("/<task_id>", methods=["GET"])
# def get_one_task(task_id):

#     task = validate_task(task_id)

    # Return should be 
    # {
    #     "task": {
    #         "id": 1,
    #         "title": "Example Task Title 1",
    #         "description": "Example Task Description 1",
    #         "is_complete": false
    #     }
    # }

    # return jsonify({"task" : 
    #     {
    #         "id" : task.task_id,
    #         "title" : task.title,
    #         "description" : task.description,
    #     }
    # })




# ---- UPDATE ONE TASK ---- #
# @tasks_bp.route("/<task_id>", methods=["GET"])
# def update_task(task_id):

#     task = validate_task(task_id)

    # Return should be 
    # {
    #     "task": {
    #         "id": 1,
    #         "title": "Example Task Title 1",
    #         "description": "Example Task Description 1",
    #         "is_complete": false
    #     }
    # }

    # return jsonify({"task" : 
    #     {
    #         "id" : task.task_id,
    #         "title" : task.title,
    #         "description" : task.description,
    #     }
    # })



# ---- DELETE ONE TASK ---- #
# @tasks_bp.route("/<task_id>", methods=["DELETE"])
# def delete_one_task(task_id):

#     task = validate_task(task_id)

#     db.session.delete(task)
#     # Commit the changes
#     db.session.commit()



    # returned response body should look like this:
    # {
    #   "details": "Task 1 \"Go on my daily walk 🏞 \" successfully deleted"
    # }

    # Need to change this response body  
    # return make_response({"details" : f'Task {task_id} successfully deleted.'}, 200)