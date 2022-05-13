from app import db
from flask import make_response, abort


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer,db.ForeignKey('goal.goal_id'),nullable=True)
    goal = db.relationship("Goal",back_populates="tasks")
    
    def to_json(self,task=True):
        response = {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)
                }
        if self.goal_id is not None:
            response["goal_id"] = self.goal_id
        if task:
            response = { 
                "task": response}
        return response

    @classmethod
    def from_json(cls,request_body):
        try:
            return cls(title=request_body["title"],
                description=request_body["description"],
                completed_at=request_body.get("completed_at",None))
        except KeyError:
            return abort(make_response({"details":"Invalid data"},400))
    
    @classmethod
    def validate_id(cls,id):
        try:
            id = int(id)
        except ValueError:
            abort(make_response({"details":"Invalid data"}, 400))
        task = cls.query.get(id)
        if not task:
            abort(make_response({"details":f"Task #{id} does not exist"}, 404))
        return task