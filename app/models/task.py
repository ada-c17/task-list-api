from app import db


# name - The name of the task
# description - A text description of the task
# completed_at - The date, saved as text, in which the task was completed.


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime,default=None,nullable=True)
    goals = db.relationship("Goal")
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    # is_complete=db.Column(db.String,default=False)

    #why to json
    def to_json(self):
        if self.completed_at:
            is_completed=True
        else:
            is_completed=False
        task_dict= {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_completed,
        }
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict

    def to_json_without_des(self):
        if self.completed_at:
            is_completed=True
        else:
            is_completed=False
        return  {
            "id": self.task_id,
            "title": self.title,
            "description": "",
            "is_complete": is_completed,
        }

    def to_jsonn(self):
        if self.completed_at:
            is_completed=True
        else:
            is_completed=False
        return  {
            "goal_id":self.goal_id,
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_completed,
        }