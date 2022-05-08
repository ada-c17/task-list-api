from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    # __tablename__ = "books" #This is optional for if you want to plurally name your table 

def to_dict(self):
    return to_dict(
        task_id=self.task_id,
        title=self.title,
        description=self.description,
        is_complete=self.completed_at is not None
        )

@classmethod
def from_dict(cls, data_dict):
    return cls(
        title=data_dict["title"],
        description=data_dict["description"],
        completed_at=data_dict["completed_at"]
)