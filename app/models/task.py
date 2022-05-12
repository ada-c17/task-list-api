from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)

    def to_dict(self):
        return{
            "id" : self.task_id,
            "title" : self.title,
            "description" : self.description,
            "is_complete": bool(self.completed_at),
            "goal_id" : self.goal_id}



