import requests
import os

url = f"https://{os.environ.get('api')}"

def parse_response(response):
    if response.status_code >= 400:
        return None
    
    return list(response.json().values())[0]

def create_task(title, description, completed_at=None):
    query_params = {
        "title": title,
        "description": description,
        "completed_at": completed_at
    }
    response = requests.post(url+"/tasks",json=query_params)
    return parse_response(response)

def list_tasks():
    response = requests.get(url+"/tasks")
    return response.json()

def get_task(id):
    response = requests.get(url+f"/tasks/{id}")
    if response.status_code != 200:
        return None
        
    return parse_response(response)

def update_task(id,title,description):

    query_params = {
        "title": title,
        "description": description
    }

    response = requests.put(
        url+f"/tasks/{id}",
        json=query_params
        )

    return parse_response(response)

def delete_task(id):
    response = requests.delete(url+f"/tasks/{id}")
    return response.json()

def mark_complete(id):
    response = requests.patch(url+f"/tasks/{id}/mark_complete")
    return parse_response(response)

def mark_incomplete(id):
    response = requests.patch(url+f"/tasks/{id}/mark_incomplete")
    return parse_response(response)

def create_goal(title):
    query_params = {
        "title": title
    }
    response = requests.post(url+"/goals",json=query_params)
    return parse_response(response)

def list_goals():
    response = requests.get(url+"/goals")
    return response.json()

def get_goal(id):
    response = requests.get(url+f"/goals/{id}")
    if response.status_code != 200:
        return None
        
    return parse_response(response)

def update_goal(id,title):

    query_params = {
        "title": title
    }

    response = requests.put(
        url+f"/goals/{id}",
        json=query_params
        )
    
    return parse_response(response)

def delete_goal(id):
    response = requests.delete(url+f"/goals/{id}")
    return response.json()

def assign_tasks_to_goal(id, task_ids):

    query_params = {
        "task_ids": task_ids
    }

    response = requests.post(
        url+f"/goals/{id}/tasks",
        json=query_params
        )
    
    return parse_response(response)