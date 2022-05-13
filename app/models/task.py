import datetime
from app import db
from app.models.goal import Goal


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    is_complete = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey(Goal.goal_id))

    def task_to_dict(self):
        if self.goal_id:
            return dict(
                id=self.id,
                title=self.title,
                description=self.description,
                is_complete=self.is_complete,
                goal_id = self.goal_id
            )
        else:
            return dict(
                id=self.id,
                title=self.title,
                description=self.description,
                is_complete=self.is_complete)
    
    @classmethod
    def from_dict(cls, data_dict):
        if "completed_at" in data_dict:
            return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            is_complete=True,
            completed_at=data_dict["completed_at"]
            )
        else:
            return cls(
            title=data_dict["title"],
            description=data_dict["description"]
            )
    
    def replace_details(self, data_dict):
        self.title=data_dict["title"]
        self.description=data_dict["description"]
        self.is_complete=False
        if "completed_at" in data_dict:
            self.completed_at=data_dict["completed_at"]
            self.is_complete=True
        return self

    def mark_done(self):
        self.is_complete = True
        current_time = datetime.datetime.now()
        self.completed_at = current_time
        return self

    def mark_not_done(self):
        self.is_complete = False
        self.completed_at = None
        return self