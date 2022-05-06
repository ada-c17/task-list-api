from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None, nullable = True)

    def to_json(self):
        return {"id": self.task_id, 
                "title": self.title, 
                "description": self.description, 
                "is_complete": False}