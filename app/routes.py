import requests
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime, timezone
from flask import Blueprint, jsonify, make_response, request, abort
import os
# from .routes_helper import error_message


bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

# def validate_record_id(task_id):
#         try:
#                 task_id = int(task_id)
#         except:
#                 return abort(make_response({"message":f"Task {task_id} invalid"}, 400))

#         task = Task.query.get(task_id)

#         if not task:
#                 abort(make_response({"message":f"Task {task_id} not found"}, 404))

#         return task


def error_message(message, status_code):
        abort(make_response(jsonify(dict(message=message)), status_code))

def validate_record_id(cls, id):
        try:
                id = int(id)
        except:
                return abort(make_response({"message":f"{cls} {id} invalid"}, 400))

        model = cls.query.get(id)

        # if not model: 
        #         abort(make_response({"message":f"{cls}{id} not found"}, 404))
        # return model
        if model:
                return model

        # error_message(f"No model of type {cls} with id {id} found", 404)
        error_message(f"{cls.__name__} {id} not found", 404)

#POST/tasks
@bp.route("", methods=["POST"]) #methods=("POST",)) whye?
def create_task():
        request_body = request.get_json()
        if ("description" not in request_body or
                "title" not in request_body):
        
                # raise KeyError('Invalid data')
                return jsonify({"details": "Invalid data"}), 400 

        new_task = Task(
                title=request_body["title"],
                description=request_body["description"],
                completed_at=request_body.get("completed_at"))
        # new_task = Task.from_dict(request_body) #this is use for classmethod
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"task": new_task.to_json()}), 201

#GET/tasks
@bp.route("", methods=("GET",))
def get_all_tasks():
        title_param = request.args.get("title")
        sort_param = request.args.get("sort")

        if title_param:
                tasks = Task.query.filter_by(title=title_param)
        else:
                tasks = Task.query.all()

        result_list = [task.to_json() for task in tasks]
        if sort_param == "asc":
                result_list.sort(key = lambda task : task.get("title"))
                #def get_title(task):
                        #return task.get("title")

        if sort_param == "desc":
                result_list.sort(reverse = True, key = lambda task : task.get("title"))
        # tasks_response = []
        # for task in tasks:
        # tasks_response.append(task.to_json())

        return jsonify(result_list), 200

# GET /tasks/<task_id>
@bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
        task = validate_record_id(Task,task_id)
        return jsonify({"task": task.to_json()})

# PUT /tasks/<task_id>
@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
        task = validate_record_id(Task, task_id)
        request_body = request.get_json()
        request_body_keys = request_body.keys()

        if "title" in request_body_keys:
                task.title = request_body["title"]
        if "description" in request_body_keys:
                task.description = request_body["description"]
        # if "is_complete" in request_body_keys:
        #         task.is_complete = request_body["is_complete"]
        

        # task.name = request_body["name"]
        # task.description = request_body["description"]
        
        db.session.commit()
        return jsonify({"task": task.to_json()}), 200

# DELETE/tasks/<task_id>
@bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
        task = validate_record_id(Task, task_id)
        
        db.session.delete(task)
        db.session.commit()

        return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200      

@bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_on_incomplete_task(task_id):
        task = validate_record_id(Task,task_id)

        if task.completed_at is None:
                task.completed_at = datetime.now(timezone.utc)

        db.session.commit()

        send_slack_task_notification(task)
        return jsonify({"task": task.to_json()}), 200

def send_slack_task_notification(task):
        
        SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
        text = f"Someone just completed the task {task.title}"
        url = f"https://slack.com/api/chat.postMessage?channel=task-notifications&text={text}"

        data = ""

        headers = {
                'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
        }

        return requests.post(url, headers=headers, data=data)

        


@bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_on_complete_task(task_id):
        task = validate_record_id(Task,task_id)

        if task.completed_at is not None:
                task.completed_at = None

        
        db.session.commit()

        return jsonify({"task": task.to_json()}), 200
        
        # from datetime import datetime
        # task= Task.query.get(id)
        # task.completed_at = datetime.now()


#POST/goals
@goal_bp.route("", methods=["POST"])
def create_goal():
        request_body = request.get_json()
        if ("title" not in request_body):
                # raise KeyError('Invalid data')
                return jsonify({"details": "Invalid data"}), 400   

        new_goal = Goal(title=request_body["title"])
        
        db.session.add(new_goal)
        db.session.commit()

        return jsonify({"goal": new_goal.to_json()}), 201

#GET/goals
@goal_bp.route("", methods=["GET"])
def get_all_goals():
        all_goals = Goal.query.all()
        goals_as_dicts = [goal.to_json() for goal in all_goals]

        return jsonify(goals_as_dicts), 200


#GET /goals/<goal_id>
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
        
        goal = validate_record_id(Goal, goal_id)
        return jsonify(goal=goal.to_json())

# PATCH /goals/<goal_id>
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
        goal = validate_record_id(Goal, goal_id)
        request_body = request.get_json()
        request_body_keys = request_body.keys()

        if "title" in request_body_keys:
                goal.title = request_body["title"]
        
        db.session.commit()

        # goal_dict = {"goal":{
        #         "id": goal.goal_id,
        #         "title": goal.title}}

        # return make_response(jsonify(goal_dict), 200) 
        return jsonify({"goal": goal.to_json()}), 200

# DELETE/goals/<goal_id>
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
        goal = validate_record_id(Goal, goal_id)
        
        db.session.delete(goal)
        db.session.commit()

        return jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200      


#POST/goals/<goal_id>/tasks
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
        goal = validate_record_id(Goal, goal_id) 
        #Goal.query.validate_record(goal_id)
        request_body = request.get_json()  
                
        for task_id in request_body["task_ids"]:
                new_task = Task.query.get(task_id)
                new_task.goal_id = goal_id

        db.session.commit()
        print(goal.tasks)
        task_id_list = []
        for task in goal.tasks:
                task_id_list.append(task.task_id)

        return {"id": goal.goal_id, "task_ids": task_id_list}, 200
        
#GET/goals/<goal_id>/tasks
@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(goal_id):
        goal = validate_record_id(Goal, goal_id) 
        tasks_info = [task.to_json() for task in goal.tasks]
        print(tasks_info)
        return jsonify({"id": goal.goal_id, "title": goal.title, "tasks": tasks_info}), 200

        


