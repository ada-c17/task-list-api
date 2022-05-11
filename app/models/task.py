from datetime import datetime
from app import db



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None, nullable=True)
    
    def to_json(self):
        # complete = None
        # if self.completed_at == None:
        #     complete = False
        # else:
        #     complete = True
        is_complete = True if self.completed_at else False
        return {
                "id":self.id,
                "title":self.title,
                "description":self.description,
                "is_complete":is_complete
                }

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

    def update(self, req_body):
        self.title = req_body["title"]
        self.description = req_body["description"]

    def patch_to_complete(self, req_body):
        self.completed_at = datetime.now()
       
    def patch_to_incomplete(self, req_body):
        self.completed_at = None

    @classmethod
    def create_completed_at(cls, req_body):
        new_task = cls(
            title = req_body["title"],
            description = req_body["description"],
            completed_at = req_body["completed_at"]
        )
        return new_task