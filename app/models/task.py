from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None)
    #(- Nullable=True is default)
    # is_complete = db.Column(db.Datetime, default=False)

    def to_json(self):
        if not self.completed_at:
            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": False
            }
        else:
            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": True
            }
        
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
    

    
    
