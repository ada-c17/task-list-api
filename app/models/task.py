from app import db
from flask import abort, make_response


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")

    def make_task_dict(self):
        task_dict = {
                "id": self.id,
                "title": self.title,
                "description": self.description,
        }
        if self.completed_at:
            task_dict["is_complete"] = True
        else:
            task_dict["is_complete"] = False

        return task_dict

    @classmethod
    def validate_task(cls, task_id):
        try:
            task_id = int(task_id)
        except:
            abort(make_response({"Message":f"Task {task_id} invalid"}, 400))

        task = Task.query.get(task_id) 

        if not task:
            abort(make_response({"Message":f"Task {task_id} not found"}, 404))

        return task
