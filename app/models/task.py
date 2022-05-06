from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_json(self):
        if not self.completed_at:
            is_complete = False

            return {"id" : self.task_id,
                    "title" : self.title,
                    "description" : self.description,
                    "is_complete" : is_complete}


    @classmethod
    def from_json(cls, request_body):
        new_task = cls(
            title=request_body['title'],
            description=request_body['description']
            )
        return new_task


