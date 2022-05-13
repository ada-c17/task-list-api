from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id=db.Column(db.Integer, db.ForeignKey('goal.goal_id')) #a goal has many tasks, so create foreign id at task side
    goal=db.relationship("Goal", back_populates = "tasks")

    def to_json(self):
        dict= { "id": self.task_id,  
                "title": self.title,
                "description": self.description,
                "is_complete": True if self.completed_at else False,
                # "goal_id": self.goal_id if self.goal_id else None
            }
        if self.goal_id:
            dict["goal_id"] = self.goal_id
        return dict
        

    def update(self, req_body):
        self.title = req_body["title"]
        self.description = req_body["description"]
        
    @classmethod
    def create(cls, req_body):
        new_task = cls(
            title = req_body["title"],
            description = req_body["description"],
            completed_at= req_body.get("completed_at",None)
        )

        return new_task

