from flask import jsonify, abort, make_response


def error_message(message, status_code):
    abort(make_response(jsonify(dict(message=message)), status_code))

def validated_task(cls, task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        error_message(f"Invalid id {task_id}", 400)

    task = cls.query.get(task_id)
    if task:
        return task

    error_message(f"Task {task_id} not found", 404)

def validated_goal(cls, goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        error_message(f"Invalid id {goal_id}", 400)

    goal = cls.query.get(goal_id)

    if goal:
        return goal

    error_message(f"Goal {goal_id} not found", 404)




    