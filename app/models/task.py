
from app import db
# import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)

    def to_json(self):
        # change name to_dict(self):
        is_complete = False
        # if (self.completed_at is not None):
        if (self.completed_at is not None):
            is_complete = True
        return {
            # "task_id": self.task_id, 
            "id": self.task_id, 
            "title": self.title,
            "description": self.description, 
            "is_complete": is_complete
        }

    def update(self, req_body):
        self.title = req_body["title"]
        self.description = req_body["description"]
        # self.completed_at = req_body["is_complete"]
        # check to see if this needs to be here or not

    @classmethod
    def create(cls, req_body):
        if "completed_at" in req_body:
            new_task = cls(
                    title=req_body["title"],
                    description=req_body["description"],
                    completed_at=req_body["completed_at"]
                    )
        else:
            new_task = cls(
                        title=req_body["title"],
                        description=req_body["description"]
                        )
        return new_task
