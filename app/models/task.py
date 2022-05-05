from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_dict(self):
        if self.completed_at == None:
            self.completed_at = False

        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at
        )