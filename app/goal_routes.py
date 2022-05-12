from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app import db
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
import os 


goals_bp = Blueprint ('goals_bp', __name__, url_prefix = '/goals')

def validate_input(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({'details': 'Invalid goal id'}, 400))
    goals = Goal.query.all()
    for goal in goals:
        if goal_id == goal.goal_id:
            return goal
    abort(make_response ({'details': 'This goal id does not exist'}, 404))

@goals_bp.route("", methods=['GET'])
def get_all_goals():
    title_query = request.args.get('title')
    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    else:
        goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(
            {
            'id' :goal.goal_id,
            'title': goal.title,
            }), 200
            
    return jsonify(goals_response)

@goals_bp.route('/<goal_id>',methods = ['GET'])
def get_one_goal(goal_id):
    goal = validate_input(goal_id)
    response_body = {'goal':{
        'id' :goal.goal_id,
        'title': goal.title }}
    return jsonify(response_body), 200

@goals_bp.route('',methods = ['POST'])
def create_a_goal():
    request_body = request.get_json()
    if not 'title' in request_body:
        return ({'details': 'Invalid data'}, 400)
    else:
        new_goal = Goal(title=request_body['title'])
    
    db.session.add(new_goal)
    db.session.commit()

    return {'goal': {  
            'id' :new_goal.goal_id,
            'title': new_goal.title}} , 201


@goals_bp.route('/<goal_id>', methods = ['PUT'])
def update_one_goal(goal_id):
    validate_input(goal_id) 
    chosen_goal = Goal.query.get(goal_id)
    request_body = request.get_json()
    try:
        chosen_goal.title = request_body['title']
    except KeyError:
        return {'msg':'title goal required'} ,404

    db.session.commit()
    
    return {'goal': {  
            'id' :chosen_goal.goal_id,
            'title': chosen_goal.title}} , 200


@goals_bp.route('/<goal_id>',methods = ['DELETE'])
def delete_goal(goal_id):
    validate_input(goal_id)
    chosen_goal = Goal.query.get(goal_id)
    
    db.session.delete(chosen_goal)
    db.session.commit()

    return{'details':f'Goal {chosen_goal.goal_id} "{chosen_goal.title}" successfully deleted'}, 200


@goals_bp.route("/<goal_id>/tasks", methods=['POST'])
def create_task(goal_id):

    goal = validate_input(goal_id)

    request_body = request.get_json()
    new_task = Task(
        itle=request_body['title'],
        description=request_body['description'],
        completed_at = request_body['completed_at']
    )
    db.session.add(new_task)
    db.session.commit()
    return make_response(jsonify(f"Book {new_task.title} by {new_task.goal.title} successfully created"), 201)

@goals_bp.route("/<goal_id>/tasks", methods=['GET'])
def get_tasks(goal_id):

    goal = validate_input(goal_id)

    task_response = []
    for task in goal.tasks:
        task_response.append(
            {
            "id": task.id,
            "title": task.title,
            "completed at": task.completed_at,
            "goal": goal.title
            }
        )
    
    return jsonify(task_response)

