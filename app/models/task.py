from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True,    )
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None)
    # (- Nullable=True is default)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")



    def to_json(self):

            to_json_dict = {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": True if self.completed_at else False
            }
            if self.goal_id:
                to_json_dict["goal_id"] =self.goal_id

            return to_json_dict
        
    @classmethod
    def create(cls, req_body):
        if not "completed_at" in req_body:
            completed_at_status = None
        else:
            completed_at_status = req_body["completed_at"]

        new_task = cls(
            title = req_body["title"],
            description = req_body["description"],
            completed_at = completed_at_status
            
        )
        return new_task


    def update(self, req_body):
        
        if not "completed_at" in req_body:
            completed_at_status = None
        else:
            completed_at_status = req_body["completed_at"]

        
        self.title = req_body["title"],
        self.description = req_body["description"],
        self.completed_at = completed_at_status
    

    
    
