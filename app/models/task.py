from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    is_complete = db.Column(db.Boolean, default=False)

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
                "completed_at": self.completed_at,
                "is_complete": True
            }
        
    @classmethod
    def create(cls, req_body):
        new_task = cls(
            title = req_body["title"],
            description = req_body["description"],
            completed_at = None
            
        )
        return new_task
    
    def update(self, req_body):
        self.title = req_body["title"],
        self.description = req_body["description"]
        self.completed_at = None