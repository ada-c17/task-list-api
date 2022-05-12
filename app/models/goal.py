from urllib import response
from app import db
from app.models.task import Task


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def to_json_task(self):
        response = {
            "id": self.goal_id,
            "title": self.title,
            "tasks": []
        }
        return response

    def to_json(self):
        response = {"goal": {
            "id": self.goal_id,
            "title": self.title}}
        return response

    @classmethod
    def create(cls, request_body):
        new_goal = cls(
            title=request_body['title'])
        return new_goal
