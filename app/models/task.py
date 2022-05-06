from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def create(cls, request_body):
        new_task = cls(
            title=request_body['name'],
            description=request_body['description'],
        )
        return new_task
