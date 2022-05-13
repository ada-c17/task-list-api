from flask import jsonify, abort, make_response, request
from app.models.goal import Goal
from app.models.task import Task

def validate_task(task_id):
    try:
        task_id = int (task_id)
    except ValueError:
        rsp =  {"msg": f"Invalid id:{task_id}"}
        abort( make_response (jsonify(rsp), 400))
        
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        abort( make_response({"massage": f" task {task_id} not found"}, 404))
    
    return chosen_task


def validate_goal(goal_id):
    try:
        goal_id = int (goal_id)
    except ValueError:
        rsp =  {"msg": f"Invalid id:{goal_id}"}
        abort( make_response (jsonify(rsp), 400))
        
    chosen_goal = Goal.query.get(goal_id)

    if chosen_goal is None:
        abort( make_response({"massage": f" Goal {goal_id} not found"}, 404))
    
    return chosen_goal


