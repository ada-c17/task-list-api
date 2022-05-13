from datetime import datetime
from dotenv import load_dotenv
import requests
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
import os

load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def send_slack_message(task, message):
    '''
    send slack message with task information - use when marking tasks complete/incomplete
    '''
    slack_url = "https://slack.com/api/chat.postMessage?channel=task-notifications&text="
    if message == "completed":
        send_message = f"Someone just completed the task {task.title}"
    else: 
        send_message = f"The task {task.title} sent: {message}"

    try: 
        url = slack_url+send_message
        header_authorization = "Bearer "+os.environ.get("SLACK_AUTH_KEY")
        headers = {'Authorization': header_authorization}
        requests.post(url, headers=headers)
        return
    except TypeError:
        return TypeError("Slack Auth Key may be missing or invalid. Check your environment variables.")
    except:
        return 

## Task Validation & Routes


def validate_tasks(input_id):
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
        
        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]

        db.session.add(new_task)
        db.session.commit()
        # db.session.expire(new_task)

        return make_response(jsonify(new_task.single_dict()), 201)

    except KeyError:
        return make_response(jsonify({"details":"Invalid data"}), 400)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_query = request.args.get("is_complete")

    if title_query:
        tasks = Task.query.filter(Task.title.ilike("%" + title_query + "%"))
    elif description_query:
        tasks = Task.query.filter(Task.description.ilike("%" + description_query + "%"))
    elif completed_query == "false":
        tasks = Task.query.filter(Task.completed_at == None)
    elif completed_query == "true":
        tasks = Task.query.filter(Task.completed_at != None)
    elif sort_query in ("asc","desc"):
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
    task = validate_tasks(task_id)

    return make_response(jsonify(task.single_dict()), 200)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_tasks(task_id)
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
            send_slack_message(task, "completed")
        elif request_body["is_complete"] == False:
            task.completed_at = None
            send_slack_message(task, "marked incomplete")

    db.session.commit()
    # db.session.expire(task)

    return make_response(jsonify(task.single_dict()), 200)

@tasks_bp.route("/<task_id>/<mark_completion>", methods=["PATCH"])
def task_completion(task_id, mark_completion):
    task = validate_tasks(task_id)

    if mark_completion == "mark_complete":
        task.completed_at = datetime.utcnow()
        send_slack_message(task, "completed")
    elif mark_completion == "mark_incomplete":
        task.completed_at = None
        send_slack_message(task, "marked incomplete")
    else:
        abort(make_response({"message":f"please use mark_complete or mark_incomplete"}, 404))
    
    db.session.commit()
    return make_response(jsonify(task.single_dict()), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_tasks(task_id)
    
    response = {"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify(response), 200)
    

## Goal Validation & Routes:


def validate_goals(input_id):
    try:
        int_id = int(input_id)
    except:
        abort(make_response({"message":f"Goal {input_id} invalid"}, 400))
    goal = Goal.query.get(int_id)
    if not goal:
        abort(make_response({"message":f"Goal {int_id} not found"}, 404))
    return goal


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    # sort_query = request.args.get("sort")
    # title_query = request.args.get("title")

    # if title_query:
    #     tasks = Task.query.filter(Task.title.ilike("%" + title_query + "%"))
    # elif description_query:
    #     tasks = Task.query.filter(Task.description.ilike("%" + description_query + "%"))
    # elif completed_query == "false":
    #     tasks = Task.query.filter(Task.completed_at == None)
    # elif completed_query == "true":
    #     tasks = Task.query.filter(Task.completed_at != None)
    # elif sort_query in ("asc","desc"):
    #     if sort_query == "asc":
    #         tasks = Task.query.order_by(Task.title).all()
    #     else:
    #         tasks = Task.query.order_by(Task.title.desc()).all()
    # else: 
    
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return make_response(jsonify(goals_response), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goals(goal_id)

    return make_response(jsonify(goal.single_dict()), 200)


@goals_bp.route("", methods=["POST"])
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal(
            title=request_body["title"]
            )

        db.session.add(new_goal)
        db.session.commit()

        return make_response(jsonify(new_goal.single_dict()), 201)

    except KeyError:
        return make_response(jsonify({"details":"Invalid data"}), 400)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_goals(goal_id)
    request_body = request.get_json()
    request_body_keys = request_body.keys()

    if "title" in request_body_keys:
        goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify(goal.single_dict()), 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goals(goal_id)
    
    response = {"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify(response), 200)



@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = validate_goals(goal_id)
    request_body = request.get_json()
    request_body_keys = request_body.keys()
    task_ids = []
    if "task_ids" in request_body_keys:
        for task_id in request_body["task_ids"]:
            task_ids.append(validate_tasks(task_id))
    print(task_ids)
    goal.tasks = task_ids

    db.session.commit()

    response_body = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
        }
    return make_response(response_body, 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_assigned_to_goal(goal_id):
    goal = validate_goals(goal_id)
    # tasks = goal.tasks
    # print(tasks)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(Task.to_dict(task))
    response = goal.dict_with_tasks()
    response["tasks"] = tasks_response

    return make_response(jsonify(response), 200)

