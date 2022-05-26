from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, nullable = False)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    completed_at = db.Column(db.DateTime, nullable = True)

    def to_dict(self):
        return dict(
            id = self.task_id,
            title = self.title,
            description = self.description,
            is_complete = bool(self.completed_at)
            )

    def one_task_to_dict(self):
        result = {}
        result["task"] = self.to_dict()
        return result

    def replace_details(self, data_dict):
        self.title = data_dict["title"]
        self.description = data_dict["description"]
