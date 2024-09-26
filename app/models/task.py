from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = True)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable = True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):
        task_dict = {
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "is_complete": True if self.completed_at else False
            }
        
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        
        return task_dict

    def update(self, request_body):
        self.title=request_body["title"]
        self.description=request_body["description"]
    
    @classmethod
    def create(cls, request_body):
        return cls(
            title=request_body["title"],
            description=request_body["description"],
            completed_at = request_body.get("completed_at", None))