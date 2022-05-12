from requests import request
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)


    def to_dict(self):
        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=True if self.completed_at else False
            # is_complete=self.completed_at is not None
        )


    @classmethod
    def from_dict(cls, data_dict):
        return cls(
                title=data_dict["title"],
                description=data_dict["description"],
                # completed_at = True if data_dict["completed_at"] else None)
                completed_at = data_dict.get("completed_at", None))
        

    def override_task(self, data_dict):
        self.title = data_dict["title"]
        self.description = data_dict["description"]