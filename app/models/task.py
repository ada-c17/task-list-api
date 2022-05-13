from app import db
# from datetime import datetime
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")
    # __tablename__ = "tasks" #This is optional for if you want to plurally name your table 

    def to_dict(self):
        if self.goal_id is None:
            return dict(
                id=self.task_id,
                title=self.title,
                description=self.description,
                is_complete= True if self.completed_at else False
                )
        else:
            return dict(
                id=self.task_id,
                title=self.title,
                description=self.description,
                goal_id=self.goal_id,
                is_complete= True if self.completed_at else False
                ) 


    def update(self,request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
    
    @classmethod
    def create(cls, request_body):
        return cls(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body.get("completed_at", None) 
            #This value returns None if there is no argument
            # .get is a dictionary method. 
            )






