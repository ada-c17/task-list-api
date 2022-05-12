from flask import abort, make_response
import requests
import os 

def validate_model_instance(cls, model_id, class_name):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{class_name} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)    
    if not model: 
        return abort(make_response({"message":f"{class_name} {model_id} not found"}, 404))
        
    return model

def send_slack_completed_message(task):

    PATH = "https://slack.com/api/chat.postMessage"

    API_KEY = os.environ.get(
            "SLACK_API_KEY")
    BEARER_TOKEN = os.environ.get(
            "AUTH_TOKEN_SLACK")

    query_params = {"channel" : "task-notifications", "text": f'Someone just completed the task {task.title}' }
    headers = {"authorization" : BEARER_TOKEN}
    
    response_body = requests.get(PATH, params=query_params, headers=headers)


# def validate_goal(goal_id):
#     try:
#         goal_id = int(goal_id)
#     except:
#         abort(make_response({"message":f"goal {goal_id} invalid"}, 400))

#     goal = Goal.query.get(goal_id)    
#     if not goal: 
#         return abort(make_response({"message":f"goal {goal_id} not found"}, 404))
            
#     return goal
