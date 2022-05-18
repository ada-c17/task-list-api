from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        return dict(
            id=self.goal_id,
            title=self.title
            )

    def update(self,request_body):
        self.title = request_body["title"]
    
    @classmethod
    def create(cls, request_body):
        return cls(
            title=request_body["title"]
            )



