from app import db
from flask import current_app, abort, make_response


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates = "tasks")


    def make_json(self):
        if not self.completed_at:
            is_complete = False
        else:
            is_complete = True
        if self.goal_id:
            return {"id": self.task_id,
            "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
        else: 
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": is_complete
            }

    @classmethod
    def valid_task(cls, request_body):
        try:
            new_task = cls(
            title=request_body['title'],
            description=request_body['description'],
            completed_at=request_body['completed_at'])
        except KeyError: 
            new_task = cls(
            title=request_body['title'],
            description=request_body['description'],)
        return new_task
 
