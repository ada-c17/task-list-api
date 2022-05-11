from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def task_response(self):

        is_complete = True if self.completed_at else False

        return {
                'id': self.task_id,
                'title': self.title,
                'description': self.description,
                'is_complete': is_complete
                }