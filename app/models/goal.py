from sqlalchemy import null
from app import db
from app.handler import Handler


class Goal(db.Model, Handler):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", backref='goal', lazy=True)

    def to_dict(self):
        return dict(
            id = self.id,
            title = self.title
        )
        
    def to_dict_with_tasks(self):
        return dict(
                id = self.id,
                title = self.title,
                tasks = [task.to_dict() for task in self.tasks]
            )

    @classmethod
    def from_dict(cls, data_dict):
        return cls(title=data_dict["title"])