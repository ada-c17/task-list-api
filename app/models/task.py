from datetime import datetime
from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None, nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)

    def to_json(self):
        is_complete = True if self.completed_at else False 
        task_dict = {
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "is_complete":is_complete,
            }
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict

    @classmethod
    def create(cls, req_body):
        if "completed_at" in req_body:
            new_task = cls(
                title = req_body["title"],
                description = req_body["description"],
                completed_at = req_body["completed_at"]
            )
        else:
            new_task = cls(
                title = req_body["title"],
                description = req_body["description"]
            )
            
        return new_task

    @classmethod
    def create_completed_at(cls, req_body):
        return cls(
            title = req_body["title"],
            description = req_body["description"],
            # completed_at = req_body["completed_at"])
            completed_at = req_body.get("completed_at", None))
            # I don't know which one would be better between line 45 and 46, both are passing tests.
    
    def update(self, req_body):
        self.title = req_body["title"]
        self.description = req_body["description"]

    def patch_to_complete(self):
        self.completed_at = datetime.utcnow()
       
    def patch_to_incomplete(self):
        self.completed_at = None
