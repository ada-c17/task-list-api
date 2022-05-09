from app import db
from flask import request, abort,make_response

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
    goal = db.relationship("Goal", back_populates = "tasks", lazy = True)
    
    def task_to_JSON(self):
        rsp = {"task":
            {"id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at),
        }}
        if self.goal_id:
            rsp["task"]["goal_id"] = self.goal_id
        
        return rsp
    
    @staticmethod
    def task_from_JSON():
        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body:
            abort(make_response({"details":"Invalid data"},400))

        if "completed_at" in request_body:
            task = Task(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = request_body["completed_at"])
        else:
            task = Task(title = request_body["title"],
                        description = request_body["description"])
        return task