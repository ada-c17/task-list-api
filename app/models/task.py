from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))

    def to_dict(self):
        dct = {
            "id":self.task_id,
            "title":self.title,
            "description":self.description,
            "is_complete":bool(self.completed_at),
        }

        if self.goal_id:
            dct["goal_id"] = self.goal_id

        return dct
