from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response,request					
from app import db	
from datetime import datetime, date, time, timezone
import requests
import os
# import app.models.goal import Goal


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")	

# Helper Function
def validate_task(id):
    try:
        task_id = int(id)
    except ValueError:
            abort(make_response(jsonify(dict(details=f"Invalid id {task_id}")), 400))
 

    task = Task.query.get(id)
    if task:
        return task

    abort(make_response(jsonify(dict(details=f"No task with id {id} found")), 404))   
					

# CREATE NEW TASK
@tasks_bp.route("", methods=[ "POST"])						
def create_task():		
						
    request_body = request.get_json()	
    try:					
        new_task = Task(						
            title=request_body["title"],					
            description=request_body["description"])

        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]

    except KeyError:
        abort(make_response(jsonify(dict(details="Invalid data")), 400))
           
    
    db.session.add(new_task)  
    db.session.commit() 

    response_body = { "task":
        {   
        "id": new_task.task_id,       
        "title": new_task.title,   
        "description": new_task.description,     
        "is_complete": True if new_task.completed_at else False
        }
    }, 201
   

    return response_body	
    # return make_response(jsonify(response_body), 201)
    


# GET ONE BY ID METHOD

@tasks_bp.route("/<task_id>", methods=["GET"])
# return dictionary with "task" as key and the value is a nested dictionary

def get_task_by_id(task_id):
    task = validate_task(task_id)

    if task == None:
        return []
    response_body = { "task":
        {   
        "id": task.task_id,   
        "goal_id":task.goal_id,    
        "title": task.title,   
        "description": task.description,     
        "is_complete": True if task.completed_at else False 					
        }
    }
       
    return response_body 
    
 
   
# GET  ALL ROUTE
@tasks_bp.route("", methods=["GET"])						
def get_all_tasks():    
    
    sort_query = request.args.get("sort")

    if sort_query:
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
    else:		   			
     
        tasks = Task.query.all()

    if tasks == None:
            return []
    else:
        response_body = []
        for task in tasks:	            					
            response_body.append({					
            "id": task.task_id,					
            "title": task.title,					
            "description": task.description,
            "is_complete": True if task.completed_at else False 					
            })	
        
        return jsonify(response_body)
                        


# # Update ONE TASK
@tasks_bp.route("/<task_id>", methods=["PUT"])

def update_task_by_id(task_id):

    task = validate_task(task_id)
    request_body = request.get_json()

    # task.task_id = request_body["task_id"]    
    task.title = request_body["title"]   
    task.description = request_body["description"] 

    if request_body["completed_at"]:  
           task.completed_at = datetime.utcnow()
    # task.completed_at = request_body["completed_at"]


    response_body = { "task":
        {   
        "id": task.task_id,       
        "title": task.title,   
        "description": task.description,     
        "is_complete":True if task.completed_at else False
        }
    }
    
     
    
    db.session.commit()

    return  response_body


#Helper Function for Slack API call

def send_api_call(task_title):
    path = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API_KEY")
    
    headers = {"Authorization": f"Bearer {SLACK_API_KEY}",
    "Content-Type": "application/json"}
    json_body = {"channel":"task-notifications",
    "text": f"Someone just completed the task {task_title}"
    }

    requests.post(path, headers=headers, json=json_body)
    # data = {}
    # data=data,
    # ?channel=task-notifications&text=Someone just completed the task {title}"
#-https://slack.com/api/chat.postMessage?channel=task-notifications&text=Namaste


# Mark Complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])

def mark_complete(task_id):

    task = validate_task(task_id)
    request_body = request.get_json()

    send_api_call(task.title)

    task.completed_at = datetime.now()
     
    response_body = { "task":
        {   
        "id": task.task_id,       
        "title": task.title,   
        "description": task.description,     
        "is_complete": True if task.completed_at else False	
        }
    }, 200
   
    db.session.add(task)
    db.session.commit()

    return  response_body


# Mark Inomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])

def mark_incomplete(task_id):

    task = validate_task(task_id)
    request_body = request.get_json()

    task.completed_at = None
     
    response_body = { "task":
        {   
        "id": task.task_id,       
        "title": task.title,   
        "description": task.description,     
        "is_complete": True if task.completed_at else False	
        }
    }, 200
   
    db.session.add(task)
    db.session.commit()

    return  response_body

  # .datetime.now() to mark field with current time

    # slack message  "Someone just completed the task My Beautiful Task". 
    # Example of Slack post url -https://slack.com/api/chat.postMessage?channel=task-notifications&text=Namaste


# Delete 
@tasks_bp.route("/<task_id>", methods=["DELETE"])

def delete_task_by_id(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response_body = {
         "details": 
         f"Task {task.task_id} \ {task.description} \" successfully deleted"
    }

    return response_body
 


    
       
       
    	
    
    
