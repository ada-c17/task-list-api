from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy = True )

    @classmethod
    def make_goal(cls,request_body):
        new_goal = cls(title = request_body["title"])
            
        return new_goal

    def to_json(self):
        return {"id": self.goal_id, 
                "title": self.title}
            
    def update_goal(self, request_body):
        self.title = request_body["title"]
