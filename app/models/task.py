from flask import abort, make_response
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):
        response_body  = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description, 
            "is_complete": False if not self.completed_at else True
            }
        
        if self.goal_id: 
            response_body["goal_id"] = self.goal_id 

        return response_body

# Class method to create a new task
    @classmethod
    def create(cls, request_body):
        if "title" not in request_body or "description" not in request_body:
            abort(make_response({"details": f'Invalid data'}, 400))

        if "completed_at" not in request_body:
            new_task = cls(
                title=request_body["title"],
                description=request_body["description"]
            )
        else:
            new_task = cls(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"]
        )
        return new_task

# Method to update tasks
    def update(self, request_body):
        self.title = request_body["title"],
        self.description = request_body["description"]