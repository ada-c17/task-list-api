from sqlalchemy import null
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey(
        'goal.goal_id'), nullable=True)  # reference name of class

    # goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):
        complete = None
        if self.completed_at == None or self.completed_at == null:
            complete = False
        elif self.completed_at != None:
            complete = True
        goal = None

        response = {"task": {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": complete}}
        if self.goal_id:
            response["task"]["goal_id"] = self.goal_id
        return response

    @ classmethod
    def create(cls, request_body):
        new_task = cls(
            title=request_body['title'],
            description=request_body['description']
        )
        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]
        return new_task

    def update(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
    #     # if "completed_at" in request_body:
    #     #     self.completed_at = request_body["completed_at"]
