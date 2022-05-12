from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

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