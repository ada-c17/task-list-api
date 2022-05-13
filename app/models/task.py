from app import db
from flask import make_response, abort

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    # not sure if it's correct to add an __init__ method but without it I kept getting "TypeError: __init__() takes 1 positional argument but 4 were given"
    def __init__(self, title, description, completed_at = None):
        self.title = title 
        self.description = description
        self.completed_at = completed_at

    def is_complete(self):
        return bool(self.completed_at)

        # before refactoring
        # if not self.completed_at:
        #     return False 
        # else:
        #     return True 
    
    def to_json(self):
        json = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
        }

        if self.goal_id:
            json["goal_id"] = self.goal_id

        return json 

    # not sure if I was supposed to pass in self here, couldn't get it to work if I did
    def validate_task(task_id):
        try:
            task_id = int(task_id)
        except ValueError:
            abort(make_response({"message":f"Task {task_id} invalid"}, 400))

        
        task = Task.query.get(task_id)
        if not task:
            abort(make_response({"message":f"Task {task_id} not found"}, 404))
        
        return task 


    @classmethod
    def from_json(cls, task_json):
        title = task_json["title"]
        description = task_json["description"]

        if "completed_at" in task_json:
            completed_at = task_json["completed_at"]
            task = cls(title, description, completed_at)
        else: 
            task = cls(title, description)

        return task