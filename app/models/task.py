from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates = "tasks")

    def to_dict(self):
        task_list_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "goal_id": self.goal_id,
            "is_complete": False
        }
        return task_list_dict

    def to_dict_2(self):
        task_list_dict = {
            "goal_id": self.goal_id
        }
        return task_list_dict