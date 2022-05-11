from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime) 
    # `db.DateTime` thought this should be None...

    def to_dict(self):
        status = True if self.completed_at is not None else False
        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": status
                }
