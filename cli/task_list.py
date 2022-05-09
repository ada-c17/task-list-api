import requests

url = "http://localhost:5000"

def parse_response(response):
    if response.status_code >= 400:
        return None
    
    return response.json()["task"]

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



    
