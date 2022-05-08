from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def create(cls, req_body):
        new_task = cls(
            title=req_body["title"],
            description=req_body["description"],
            completed_at = req_body.get("completed_at")
        )
        return new_task

    def to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False

        }

    def update(self, req_body):
        self.title = req_body["title"]
        self.description = req_body["description"]
        self.completed_at = req_body.get("completed_at")