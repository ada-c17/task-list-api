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
            completed_at = (req_body["completed_at"] 
                            if req_body["completed_at"] else None)
        )
        return new_task