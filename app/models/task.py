from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = False)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description":self.description,
            "completed_at": self.completed_at
        }

    def update_task(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
        self.completed_at = request_body["completed at"]


    @classmethod
    def create_task(cls, request_body):
        new_task = cls(title = ["title"],
            description = ["description"],
            completed_at = ["completed"])
        return new_task
