from email.errors import InvalidMultipartContentTransferEncodingDefect
from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    goal = db.relationship("Goal", back_populates="tasks")


    def to_json(self):            
        rsp = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_complete': self.completed_at is not None
        }

        if self.goal_id: 
            rsp['goal_id'] = self.goal_id

        return rsp