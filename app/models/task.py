from flask import abort, make_response, request
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(280))
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def validate_task(task_id):
        '''Validates that task id is valid and exists'''
        try:
            task_id = int(task_id)
        except:
            abort(make_response({"msg": f"Invalid id: {task_id}"}, 400))
        
        task = Task.query.get(task_id)
        if not task:
            abort(make_response({"msg": f"Could not find task with id: {task_id}"}, 404))
        return task

    def is_complete(task):
        '''Checks whether a task is incomplete or complete.'''
        if task.completed_at:
            return True
        else:
            return False

    def task_response(self):
        result = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": Task.is_complete(self)
        }
        if self.goal_id:
            result["goal_id"] = self.goal_id
        return result
