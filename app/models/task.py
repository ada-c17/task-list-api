from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None, nullable = True)

    @classmethod
    def make_task(cls,request_body):
        new_task = cls(title = request_body["title"], 
                        description = request_body["description"])
        return new_task

    def to_json(self):
        is_complete = False if not self.completed_at else True
        return {"id": self.task_id, 
                "title": self.title, 
                "description": self.description, 
                "is_complete": is_complete}
    
    def update_task(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]